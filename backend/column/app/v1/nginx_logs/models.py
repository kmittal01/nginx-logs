import datetime

from mongoengine import Document, StringField, DateTimeField, IntField


class NginxLogs(Document):
    ip_address = StringField(max_length=20)
    url = StringField()
    status_code = IntField(3)
    bytes_sent = IntField()
    referrer = StringField()
    user_agent = StringField()
    sha_256 = StringField()
    created_at = DateTimeField(default=datetime.datetime.utcnow())
