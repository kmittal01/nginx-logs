import typing as t

from fastapi import APIRouter, Response

from . import schemas
from .controller import (create_log, list_nginx_logs, raw_log_list)

nginx_logs_router = r = APIRouter()


@r.get("/nginx-logs-raw", response_model=list)
async def get_log_list_raw(
        response: Response,
):
    """
    Get List of Nginx Logs of the Host Server (in readable format).
    """
    raw_log = raw_log_list()
    response.headers["Content-Range"] = f"0-9/{len(raw_log)}"
    return raw_log


@r.put("/nginx-log", response_model=t.List[schemas.NginxLog])
async def save_log_to_mongo(
        max_lines: int = 100,
):
    """
    Save Logs into DB: Inserts last 100 lines of code from nginx log to mongodb
    """
    return create_log(max_lines)


@r.get("/nginx-logs-saved", response_model=t.List[schemas.NginxLog])
async def get_log_list(
        response: Response,
        page_size: int = 100,
        page_no: int = 1
):
    """
    Get List of Nginx Logs Saved in the Database
    """
    log_list = list_nginx_logs(page_size, page_no)
    response.headers["Content-Range"] = f"0-9/{len(log_list)}"
    return log_list
