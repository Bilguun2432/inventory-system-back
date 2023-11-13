from pydantic import BaseModel, root_validator

# Model
from model.modules.auth.permission_models import AuthPermissionModel


class AuthRoleModel(BaseModel):
    id: int
    name: str
    description: str
    permissions: list[AuthPermissionModel]

    
class AuthRoleCreateModel(BaseModel):
    name: str
    description: str

    @root_validator(pre=True)
    def check_passwords_match(cls, values):
        if not isinstance(values.get('name'), str) :
            raise ValueError("name is string.")
        if not isinstance(values.get('description'), str) :
            raise ValueError("description is string.")
        return values
    

class AuthRoleUpdateModel(BaseModel):
    name: str
    description: str

    @root_validator(pre=True)
    def check_passwords_match(cls, values):
        if not isinstance(values.get('name'), str) :
            raise ValueError("name is string.")
        if not isinstance(values.get('description'), str) :
            raise ValueError("description is string.")
        return values


class AuthRoleAddModel(BaseModel):
    roleId: int

    @root_validator(pre=True)
    def check_passwords_match(cls, values):
        if not isinstance(values.get('roleId'), int) :
            raise ValueError("roleId is Integer.")
        return values




class AuthRolePermissionModel(BaseModel):
    roleId: int
    permissionId: int