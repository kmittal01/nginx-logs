import typing as t
from ..custom_base_schemas import CustomBaseModel, CustomIdModel
from pydantic import BaseModel

to = t.Optional


class NginxLogBase(BaseModel):
    ip_address: str
    bytes_sent: int
    status_code: int
    referrer: str
    user_agent: str


class NginxLogWithDates(CustomBaseModel, NginxLogBase):
    pass


class NginxLog(NginxLogWithDates, CustomIdModel):
    pass


