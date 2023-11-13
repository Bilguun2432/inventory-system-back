from enum import Enum
from typing import Optional, List, TypeVar, Generic
from pydantic import BaseModel, root_validator
T = TypeVar('T')


#// Class validation
class AddRemoveEnum(str, Enum):
    add = "add"
    remove = "remove"


class SortTypeEnum(str, Enum):
    asc = "asc"
    desc = "desc"


class SortModel(BaseModel):
    field: Optional[str] | None = None
    sortType: Optional[SortTypeEnum] | None = None


class PaginateRequestModel(BaseModel):
    page: Optional[int]
    size: Optional[int]


class PaginateResponseModel(Generic[T], BaseModel):
    page: int
    size: int
    totalItems: int
    items: List[T]


class IdModel(BaseModel):
    id: int


class IdAddRemoveModel(BaseModel):
    id: int
    toggleType: AddRemoveEnum | None = None

    @root_validator(pre=True)
    def check_passwords_match(cls, values):
        if not isinstance(values.get('id'), int) :
            raise ValueError("id is Integer.")
        if values.get('toggleType') is not None and not values.get('toggleType') in AddRemoveEnum.__members__:
                raise ValueError("toggleType is AddRemoveEnum.",)
        return values
    
class FirebasePushNotificationModel(BaseModel):
    title: str
    body: str
    token: str
