from pydantic import BaseModel, root_validator
from typing import Optional

# Model
from model.common import PaginateRequestModel, SortModel


class AuthPermissionModel(BaseModel):
    id: int
    name: str
    permissionKey: str
    description: str
    group_name: str

    
class AuthPermissionCreateModel(BaseModel):
    name: str
    permissionKey: str
    description: str
    group_name: str

    @root_validator(pre=True)
    def check_passwords_match(cls, values):
        if not isinstance(values.get('name'), str) :
            raise ValueError("name is string.")
        if not isinstance(values.get('permissionKey'), str) :
            raise ValueError("permissionKey is string.")
        if not isinstance(values.get('description'), str) :
            raise ValueError("string is string.")
        if not isinstance(values.get('group_name'), str) :
            raise ValueError("group_name is string.")
        return values

class AuthPermissionUpdateModel(BaseModel):
    name: str
    permissionKey: str
    description: str

    @root_validator(pre=True)
    def check_passwords_match(cls, values):
        if not isinstance(values.get('name'), str) :
            raise ValueError("name is string.")
        if not isinstance(values.get('permissionKey'), str) :
            raise ValueError("permissionKey is string.")
        if not isinstance(values.get('description'), str) :
            raise ValueError("description is string.")
        return values

class AuthPermissionAddModel(BaseModel):
    permissionId: int

    @root_validator(pre=True)
    def check_passwords_match(cls, values):
        if not isinstance(values.get('permissionId'), str) :
            raise ValueError("permissionId is string.")
        return values

class AuthPermissionFilterModel(BaseModel):
    name: Optional[str] | None = None
    permissionKey: Optional[str] | None = None
    group_name: Optional[str] | None = None
    description: Optional[str] | None = None

class AuthPermissionListRequestModel(BaseModel):
    filter: AuthPermissionFilterModel
    sort: SortModel
    pagination: PaginateRequestModel
    
class AuthPermissionPaginateResponseModel(BaseModel):
    filter: AuthPermissionFilterModel
    sort: SortModel
    pagination: PaginateRequestModel
