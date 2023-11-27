from pydantic import BaseModel, root_validator


class AuthRoleModel(BaseModel):
    id: int
    name: str
    description: str

    
class AuthRoleCreateModel(BaseModel):
    name: str
    description: str
    

class AuthRoleUpdateModel(BaseModel):
    name: str
    description: str