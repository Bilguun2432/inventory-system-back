from typing import Annotated, List
from fastapi import Depends, HTTPException, APIRouter, Path
from config.database import get_db
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

# Lib
from lib import auth_service2, http
# Schema
from schema.auth_module import AuthPermission, AuthUser
# Model
from model.modules.auth.permission_models import AuthPermissionCreateModel, AuthPermissionUpdateModel, AuthPermissionModel, \
    AuthPermissionListRequestModel, AuthPermissionPaginateResponseModel
from model.common import PaginateResponseModel
# Repo
from repository.user.permission_repository import PermissionRepository


router = APIRouter(
    prefix="/auth/permission",
    tags=["AuthPermission"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


def indexAll(
    accessUser: Annotated[AuthUser, Depends(auth_service2.getAccessUser)],
    filterModel: AuthPermissionPaginateResponseModel = None,
    db: Session = Depends(get_db)
):
    authPermission_repo = PermissionRepository(db)
    authPermissions = authPermission_repo.findAll(model=filterModel)
    return http.successResponse(data = authPermissions)


@router.get('/', response_model=List[AuthPermissionModel], name="admn_auth_permission_index")
def getAll(
    accessUser: Annotated[AuthUser, Depends(auth_service2.getAccessUser)],
    filterModel: AuthPermissionPaginateResponseModel = None,
    db: Session = Depends(get_db)
):
    return indexAll(accessUser=accessUser, filterModel=filterModel, db=db)


@router.post("/", response_model=List[AuthPermissionModel], name = "admn_auth_permission_index")
def postIndex(
    accessUser: Annotated[AuthUser, Depends(auth_service2.getAccessUser)],
    filterModel: AuthPermissionPaginateResponseModel,
    db: Session = Depends(get_db)
):
    return indexAll(accessUser=accessUser, filterModel=filterModel, db=db)


@router.get('/{id}/detail', response_model=AuthPermissionModel, name="admn_auth_permission_detail")
def detail(
    id: Annotated[int, Path(title="Permission id")],
    accessUser: Annotated[AuthUser, Depends(auth_service2.getAccessUser)],
    db: Session = Depends(get_db)
):
    repo = PermissionRepository(db)
    permission = repo.findOneId(id)
    if not permission:
        raise HTTPException(status_code=404, detail="id not exists ")
    
    jsonResult = jsonable_encoder(permission)

    return JSONResponse(jsonResult)


# , response_model=AuthPermissionModel
@router.post('/create', name="admn_auth_permission_create", status_code=201 )
def create(
    model: AuthPermissionCreateModel,
    accessUser: Annotated[AuthUser, Depends(auth_service2.getAccessUser)],
    db: Session = Depends(get_db)
):
    PermissionObj = model.dict()
    repo = PermissionRepository(db)
    onePermission = repo.findOne(PermissionObj["permissionKey"])
    if(onePermission):
        raise HTTPException(status_code=404, detail="permissionKey already exists ")
    authPermission = AuthPermission(**model.dict())
    db.add(authPermission)
    db.commit()
    db.refresh(authPermission)
    print(jsonable_encoder( authPermission))
    return authPermission


@router.put('/{id}/update', response_model=AuthPermissionModel )
def update(
    id: Annotated[int, Path(title="permission id")],
    model: AuthPermissionUpdateModel,
    accessUser: Annotated[AuthUser, Depends(auth_service2.getAccessUser)],
    db: Session = Depends(get_db)
):
    repo = PermissionRepository(db)
    onePermission = repo.findOneId(id)
    if not onePermission:
        raise HTTPException(status_code=404, detail="Permission not found")
    PermissionName = repo.findOne(model.dict()['name'])
    if  PermissionName:
        raise HTTPException(status_code=404, detail="name already exists")
    onePermission.name = model.name
    onePermission.description = model.description
    onePermission.permissionKey = model.permissionKey
    db.commit()
    return JSONResponse(jsonable_encoder(repo.findOneId(id)))


@router.delete('/{id}/delete', response_model=AuthPermissionModel, name="admn_auth_permission_detail")
def delete(
    id: Annotated[int, Path(title="AuthPermission id")],
    accessUser: Annotated[AuthUser, Depends(auth_service2.getAccessUser)],
    db: Session = Depends(get_db)
):
    repo = PermissionRepository(db)
    PermissionDb: AuthPermission = repo.findOneId(id)
    if not PermissionDb:
        raise HTTPException(status_code=404, detail="AuthPermission not found")
    
    PermissionDb.isDeleted = True
    db.commit()

    jsonResult = jsonable_encoder(PermissionDb)
    return JSONResponse(jsonResult)