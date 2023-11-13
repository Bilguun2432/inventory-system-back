from pydantic import BaseModel
from enum import Enum


class NumberServiceType(str, Enum):
    prepaid = "prepaid"
    postpaid = "postpaid"


class NumberRequestModel(BaseModel):
    number: str