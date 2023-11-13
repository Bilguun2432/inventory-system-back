from typing import Annotated
from fastapi import Depends, HTTPException, APIRouter, Path
from config.database import get_db
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

# Lib
from lib import auth_service2
# Schema
from schema.auth_module import AuthRole, AuthRolePermission, AuthUser
# Model
from model.modules.auth.role_models import AuthRoleCreateModel, AuthRoleUpdateModel, AuthRoleModel, AuthRolePermissionModel
from model.modules.auth.permission_models import AuthPermissionAddModel
from model.modules.auth.user_models import AuthUserModel, AuthUserRoleModel
# Repo
from repository.user.user_repository import RoleRepository, AuthRolePermissionRepository
from repository.user.permission_repository import PermissionRepository


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
    repo = RoleRepository(db)
    permission = repo.findAll()
    return {"status": "success", "data": permission}


@router.get('/{id}', response_model=AuthRoleModel, name="admn_auth_role_detail")
def detail(
    id: Annotated[int, Path(title="role id")],
    accessUser: Annotated[AuthUser, Depends(auth_service2.getAccessUser)],
    db: Session = Depends(get_db)
):
    repo = RoleRepository(db)
    authRole = repo.findOneId(id)
    if not authRole:
        raise HTTPException(status_code=404, detail="authRole id not exists ")
    return authRole


# @router.get('/{id}', response_model=AuthRole)
# def index(
#     id: Annotated[int, Path(title="Role id")],
#     db: Session = Depends(get_db)
# ):
#     repo = RoleRepository(db)
#     Permission = repo.findOneId(id)
#     if not Role:
#         raise HTTPException(status_code=404, detail="id not exists ")
#     return jsonable_encoder(Role)


@router.post('/create' , response_model=AuthRoleModel, name="admn_auth_role_create", status_code=201)
def create(
    model: AuthRoleCreateModel,
    accessUser: Annotated[AuthUser, Depends(auth_service2.getAccessUser)],
    db: Session = Depends(get_db)
):
    RoleObj = model.dict()
    repo = RoleRepository(db)
    oneRole = repo.findOne(RoleObj["name"])
    if(oneRole):
        raise HTTPException(status_code=404, detail="name already exists ")
    authRole = AuthRole(**RoleObj)
    db.add(authRole)
    db.commit()
    db.refresh(authRole)
    return repo.findOne(RoleObj["name"])


@router.put('/{id}/update', response_model=AuthRoleModel, name="admn_auth_role_update")
def update(
    id: Annotated[int, Path(title="role id")],
    model: AuthRoleUpdateModel,
    accessUser: Annotated[AuthUser, Depends(auth_service2.getAccessUser)],
    db: Session = Depends(get_db)
):
    repo = RoleRepository(db)
    oneRole = repo.findOneId(id)
    if not oneRole:
        raise HTTPException(status_code=404, detail="Role not found")
    RoleName = repo.findOne(model.dict()['name'])
    if  RoleName:
        raise HTTPException(status_code=404, detail="name already exists")
    oneRole.name = model.name
    oneRole.description = model.description
    db.commit()
    return JSONResponse(jsonable_encoder(repo.findOneId(id)))


@router.delete('/{id}/delete', response_model=AuthRoleModel, name="admn_auth_role_delete")
def delete(
    id: Annotated[int, Path(title="AuthRole id")],
    accessUser: Annotated[AuthUser, Depends(auth_service2.getAccessUser)],
    db: Session = Depends(get_db)
):
    repo = RoleRepository(db)
    RoleDb: AuthRole = repo.findOneId(id)
    if not RoleDb:
        raise HTTPException(status_code=404, detail="AuthRole not found")
    
    RoleDb.isDeleted = True
    db.commit()

    jsonResult = jsonable_encoder(RoleDb)
    return JSONResponse(jsonResult)


#  response_model=AuthUserRoleModel
@router.post('/{id}/permission/add', response_model=AuthRolePermissionModel, name="admn_auth_role_addPermission", status_code=201)
def addPermission(
    id: Annotated[int, Path(title="Permission id")],
    model: AuthPermissionAddModel,
    accessUser: Annotated[AuthUser, Depends(auth_service2.getAccessUser)],
    db: Session = Depends(get_db)
):
    if(not RoleRepository(db).findOneId(id)):
        raise HTTPException(status_code=404, detail="Role id not exist")
    if(not PermissionRepository(db).findOneId(model.permissionId)):
        raise HTTPException(status_code=404, detail="Permission id not exist")
    if AuthRolePermissionRepository(db).findRoleAndPermission(id, model.permissionId):
        raise HTTPException(status_code=404, detail="RolePermission already exist")
    authRolePermission = AuthRolePermission(roleId=id, permissionId=model.permissionId)
    db.add(authRolePermission)
    db.commit()
    db.refresh(authRolePermission)
    return authRolePermission


@router.delete('/{id}/permission/{permissionId}/remove', response_model=AuthRolePermissionModel, name="admn_auth_role_deleteRole")
def deleteRole(
    id: Annotated[int, Path(title="AuthRole id")],
    permissionId: Annotated[int, Path(title="AuthRole id")],
    accessUser: Annotated[AuthUser, Depends(auth_service2.getAccessUser)],
    db: Session = Depends(get_db)
):
    authRolePermission =  AuthRolePermissionRepository(db).findRoleAndPermission(id, permissionId)
    if(not authRolePermission):
        raise HTTPException(status_code=404, detail="RolePermission not  exist")
    db.delete(authRolePermission)
    db.commit()
    return authRolePermission