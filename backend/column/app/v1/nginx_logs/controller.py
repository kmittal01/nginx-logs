import json
import re
from hashlib import sha256

from dateutil.parser import parse

from . import models


def add_sha256(log_dict):
    """
    Generates SHA 256 Hash of the log Dictionary
    """
    log_dict["created_at"] = str(log_dict["created_at"])
    log_dict["sha_256"] = sha256(json.dumps(log_dict).encode('utf8')).hexdigest()
    return log_dict


def create_log(max_lines) -> list:
    """
    Fetches last n lines of nginx access log file and stores it in mongo db.
    n being supplied by max_line parameter, default is 100.
    This function also creates sha_256 for every log and stores it with datapoint,
    to ensure the same database is not inserted twice.
    """
    nginx_log_list = raw_log_list(max_lines)
    nginx_log_list = [add_sha256(single_log) for single_log in nginx_log_list]
    all_sha_256_list = [single_log["sha_256"] for single_log in nginx_log_list]
    all_db_sha_256 = models.NginxLogs.objects(__raw__={"sha_256": {"$in": all_sha_256_list}}).only('sha_256')
    all_db_sha_256 = [ele["sha_256"] for ele in all_db_sha_256]
    response_list = []
    for single_nginx_log in nginx_log_list:
        if single_nginx_log["sha_256"] in all_db_sha_256:
            continue
        new_log = models.NginxLogs(**single_nginx_log).save()
        response_list.append(new_log.to_mongo().to_dict())
    return response_list


def list_nginx_logs(page_size, page_no) -> list:
    """
    Fetches Paginated Nginx Logs saved in database.
    """
    first_slice = page_size * (page_no - 1)
    last_slice = page_size * page_no
    all_logs = models.NginxLogs.objects().order_by('-created_at')[first_slice:last_slice]
    return [log.to_mongo().to_dict() for log in all_logs]


def raw_log_list(max_lines=None) -> list:
    """
    Parses the nginx access log file, and gets the data from the log datapoint with a regular expression.
    Excludes Access Logs by bots/crawlers.
    Returns logs as a list of dict, sorted by created_at.
    """
    resp_list = []
    lineformat = re.compile(
        r"""(?P<ip_address>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - - \[(?P<created_at>\d{2}\/[a-z]{3}\/\d{4}:\d{2}:\d{2}:\d{2} (\+|\-)\d{4})\] ((\"(GET|POST) )(?P<url>.+)(http\/1\.1")) (?P<status_code>\d{3}) (?P<bytes_sent>\d+) (["](?P<referrer>(\-)|(.+))["]) (["](?P<user_agent>.+)["])""",
        re.IGNORECASE)
    with open("/nginx_access_log/access.log") as fp:
        Lines = fp.readlines()
        if max_lines:
            Lines = Lines[-max_lines:]
        for line in Lines:
            data = re.search(lineformat, line)
            if data:
                datadict = data.groupdict()
                datadict["created_at"] = parse(datadict["created_at"], fuzzy=True)
                resp_list.append(datadict)
    resp_list = sorted(resp_list, key=lambda k: k['created_at'], reverse=True)
    return resp_list
