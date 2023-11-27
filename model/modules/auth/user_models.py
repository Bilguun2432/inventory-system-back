from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, root_validator

# Model
from model.common import PaginateRequestModel, SortModel
from model.modules.auth.role_models import AuthRoleModel


class AuthUserModel(BaseModel):
    id: int
    firstname: str
    lastname: str
    email: str
    mobile: str
    authRoleId: int
    
    authRole: AuthRoleModel

    
class AuthUserCreateModel(BaseModel):
    firstname: str
    lastname: str
    email: str
    mobile: str
    authRoleId: int


class AuthUserUpdateModel(BaseModel):
    firstname: str
    lastname: str
    email: str
    mobile: str
    authRoleId: int


class AuthUserPasswordResetModel(BaseModel):
    id: int
    userId: str
    token: str
    state: str
    timeCreated: datetime
    timeExpire: datetime
    
    
class AuthUserPasswordResetCreateModel(BaseModel):
    userId: str
    token: str
    state: str
    timeCreated: datetime
    timeExpire: datetime


class AuthUserPasswordResetUpdateModel(BaseModel):
    userId: str
    token: str
    state: str
    timeCreated: datetime
    timeExpire: datetime


class NewPasswordEmailModel(BaseModel):
    password: str


class NewPasswordPasswordModel(BaseModel):
    currentpassword: str
    password: str
    

class AuthUserRoleModel(BaseModel):
    userId: int
    roleId: int
    


# Filter

class AuthUserFilterModel(BaseModel):
    firstname: Optional[str] | None = None
    lastname: Optional[str] | None = None
    email: Optional[str] | None = None
    mobile: Optional[int] | None = None   


class AuthUserListRequestModel(BaseModel):
    filter: AuthUserFilterModel
    sort: SortModel
    pagination: PaginateRequestModel


class AuthUserPaginateResponseModel(BaseModel):
    filter: AuthUserFilterModel
    sort: SortModel
    pagination: PaginateRequestModel
    
class AuthUserMailModel(BaseModel):
    email: str