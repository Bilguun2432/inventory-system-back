from typing import List, Optional, Generic, TypeVar
from pydantic import BaseModel, root_validator
T = TypeVar('T')


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class AuthRequestModel(BaseModel):
    username: str
    password: str


class UserPayloadModel(BaseModel):
    id: int
    username: str
    email: str
    roles: List[int]


class TokenPayloadModel(BaseModel):
    user: UserPayloadModel
    type: str
    iat: int
    exp: int


class AuthTokensModel(BaseModel):
    access: str | None = None
    refresh: str | None = None


class AuthUserTokensModel(BaseModel):
    user: UserPayloadModel
    tokens: AuthTokensModel


class ResetPasswordEmailModel(BaseModel):
    email: str

    @root_validator(pre=True)
    def check_passwords_match(cls, values):
        if not isinstance(values.get('email'), str) :
            raise ValueError("email is string.")
        return values
    
    
class UserFilterQueryModel(BaseModel):
    firstname: Optional[str] | None = None
    lastname: Optional[str] | None = None
    userType: Optional[str] | None = None
    email: Optional[str] | None = None
    mobile: Optional[int] | None = None


class ResponseSchema(BaseModel):
    detail: str
    result: Optional[T] = None
    

class PaginationModel(BaseModel,  Generic[T]):
    total_record: Optional[int] | None =  None
    filter_count: Optional[int] | None =  None
    content: List[T]


class PaginateModel(BaseModel):
    page: Optional[int] | None = None
    limit: Optional[int] | None =  None


class UserFilterModel(BaseModel):
    filterModel: UserFilterQueryModel
    pagination:PaginateModel