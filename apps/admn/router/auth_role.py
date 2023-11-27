from typing import Annotated
from fastapi import Depends, HTTPException, APIRouter, Path
from config.database import get_db
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

# Lib
from lib import auth_service2, http
# Schema
from schema.auth_module import AuthRole, AuthUser
# Model
from model.modules.auth.role_models import AuthRoleCreateModel, AuthRoleUpdateModel, AuthRoleModel
from model.modules.auth.user_models import AuthUserModel, AuthUserRoleModel
# Repo
from repository.user.user_repository import RoleRepository


router = APIRouter(
    prefix="/auth/role",
    tags=["AuthRole"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get('/', name="admn_auth_role_index")
def index(
    accessUser: Annotated[AuthUser, Depends(auth_service2.getAccessUser)],
    db: Session = Depends(get_db)
):
    authRole_repo = RoleRepository(db)
    roles = authRole_repo.findAll()
    
    return http.successResponse(data = roles)


@router.post('/create', response_model=AuthRoleModel, name="admn_auth_role_create", status_code=201)
def create(
    model: AuthRoleCreateModel,
    accessUser: Annotated[AuthUser, Depends(auth_service2.getAccessUser)],
    db: Session = Depends(get_db)
):
    authRole_repo = RoleRepository(db)
    
    role = authRole_repo.findOneName(model.name)
    if role:
        raise HTTPException(status_code=400, detail="AuthRole name already exists")
    
    authRole = AuthRole(**model.dict())
    db.add(authRole)
    db.commit()
    db.refresh(authRole)
    
    jsonResult = jsonable_encoder(authRole)
    return JSONResponse(jsonResult)


@router.put('/{id}/update', response_model=AuthRoleModel, name="admn_auth_role_update")
def update(
    id: Annotated[int, Path(title="AuthRole id")],
    model: AuthRoleUpdateModel,
    accessUser: Annotated[AuthUser, Depends(auth_service2.getAccessUser)],
    db: Session = Depends(get_db)
):
    authRole_repo = RoleRepository(db)
    
    authRole = authRole_repo.findOneId(id)
    if not authRole:
        raise HTTPException(status_code=404, detail="AuthRole not found")
    
    AuthRoleCheck = authRole_repo.findOneName(model.name)
    if  AuthRoleCheck:
        raise HTTPException(status_code=400, detail="AuthRole name already exists")
    
    authRole.name = model.name
    authRole.description = model.description
    
    db.commit()
    db.refresh(authRole)

    jsonResult = jsonable_encoder(authRole)
    return JSONResponse(jsonResult)


@router.get('/{id}/detail', response_model=AuthRoleModel, name="admn_auth_role_detail")
def detail(
    id: Annotated[int, Path(title="role id")],
    accessUser: Annotated[AuthUser, Depends(auth_service2.getAccessUser)],
    db: Session = Depends(get_db)
):
    authRole_repo = RoleRepository(db)
    
    authRole = authRole_repo.findOneId(id)
    if not authRole:
        raise HTTPException(status_code=404, detail="authRole id not exists ")
    
    return authRole


# @router.delete('/{id}/delete', response_model=AuthRoleModel, name="admn_auth_role_delete")
# def delete(
#     id: Annotated[int, Path(title="AuthRole id")],
#     accessUser: Annotated[AuthUser, Depends(auth_service2.getAccessUser)],
#     db: Session = Depends(get_db)
# ):
#     repo = RoleRepository(db)
#     RoleDb: AuthRole = repo.findOneId(id)
#     if not RoleDb:
#         raise HTTPException(status_code=404, detail="AuthRole not found")
    
#     RoleDb.isDeleted = True
#     db.commit()

#     jsonResult = jsonable_encoder(RoleDb)
#     return JSONResponse(jsonResult)