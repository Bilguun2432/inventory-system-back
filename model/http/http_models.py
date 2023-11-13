from pydantic import BaseModel
from enum import Enum
from typing import Generic, TypeVar
T = TypeVar('T')


class ApiResponseStatusType(str, Enum):
    success = "success"
    error = "error"


class ApiResponseModel(Generic[T], BaseModel):
    status: ApiResponseStatusType
    message: str
    data: T | None