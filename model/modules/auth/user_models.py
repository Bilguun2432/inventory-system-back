from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, root_validator

# Model
from model.common import PaginateRequestModel, SortModel


class AuthUserType(str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"
    MERCHANT = "MERCHANT"
    APP = "APP"


class AuthUserRoleListModel(BaseModel):
    id: int
    name: str
    description: str


class AuthUserModel(BaseModel):
    id: int
    firstname: str
    lastname: str
    email: str
    mobile: str
    userType: AuthUserType
    timeCreated: datetime
    roles: list[AuthUserRoleListModel]

    
class AuthUserCreateModel(BaseModel):
    firstname: str
    lastname: str
    email: str
    mobile: str
    userType: AuthUserType
    # password: str

    @root_validator(pre=True)
    def check_passwords_match(cls, values):
        if not isinstance(values.get('firstname'), str) :
            raise ValueError("firstname is string.")
        if not isinstance(values.get('lastname'), str) :
            raise ValueError("lastname is string.")
        if not isinstance(values.get('email'), str) :
            raise ValueError("email is string.")
        if not isinstance(values.get('mobile'), str) :
            raise ValueError("mobile is string.")
        if values.get('userType') is not None and not values.get('userType') in AuthUserType.__members__:
            raise ValueError("userType is AuthUserType.",)
        return values


class AuthUserUpdateModel(BaseModel):
    firstname: str
    lastname: str
    email: str
    mobile: str
    userType: AuthUserType

    @root_validator(pre=True)
    def check_passwords_match(cls, values):
        if not isinstance(values.get('firstname'), str) :
            raise ValueError("firstname is string.")
        if not isinstance(values.get('lastname'), str) :
            raise ValueError("lastname is string.")
        if not isinstance(values.get('email'), str) :
            raise ValueError("email is string.")
        if not isinstance(values.get('mobile'), str) :
            raise ValueError("mobile is string.")
        if values.get('userType') is not None and not values.get('userType') in AuthUserType.__members__:
                raise ValueError("userType is AuthUserType.",)
        return values


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

    @root_validator(pre=True)
    def check_passwords_match(cls, values):
        if not isinstance(values.get('password'), str) :
            raise ValueError("password is string.")
        return values


class NewPasswordPasswordModel(BaseModel):
    currentpassword: str
    password: str

    @root_validator(pre=True)
    def check_passwords_match(cls, values):
        if not isinstance(values.get('currentpassword'), str) :
            raise ValueError("currentpassword is string.")
        if not isinstance(values.get('password'), str) :
            raise ValueError("password is string.")
        return values
    

class AuthUserRoleModel(BaseModel):
    userId: int
    roleId: int
    


# Filter

class AuthUserFilterModel(BaseModel):
    firstname: Optional[str] | None = None
    lastname: Optional[str] | None = None
    userType: Optional[str] | None = None
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