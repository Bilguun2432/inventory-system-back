from typing import Annotated, List
from fastapi import Depends, HTTPException, APIRouter, Path, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from config.database import get_db

# Lib
from lib import auth_service2, http
# Model
from model.common import PaginateResponseModel
from model.modules.auth.user_models import AuthUserCreateModel, AuthUserUpdateModel, AuthUserModel, AuthUserRoleModel
from model.modules.auth.user_models import AuthUserListRequestModel, AuthUserPaginateResponseModel, AuthUserMailModel
# Repo
from repository.user.user_repository import UserRepository, RoleRepository
# Schema
from schema.auth_module import AuthUser


router = APIRouter(
    prefix="/auth/user",
    tags=["AuthUser"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found auth"}},
)


def indexAll(
    accessUser: Annotated[AuthUser, Depends(auth_service2.getAccessUser)],
    filterModel: AuthUserPaginateResponseModel = None,
    db: Session = Depends(get_db)
):
    authUser_repo = UserRepository(db)
    authUsers = authUser_repo.findAll(model=filterModel)
    return http.successResponse(data = authUsers)


@router.get('/', response_model=List[AuthUserModel],  name="admn_auth_user_index")
def getAll(
    accessUser: Annotated[AuthUser, Depends(auth_service2.getAccessUser)],
    filterModel: AuthUserPaginateResponseModel = None,
    db: Session = Depends(get_db)
):
    return indexAll(accessUser=accessUser, filterModel=filterModel, db=db)


@router.post("/", response_model=List[AuthUserModel], name = "admn_auth_user_index")
def postIndex(
    accessUser: Annotated[AuthUser, Depends(auth_service2.getAccessUser)],
    filterModel: AuthUserPaginateResponseModel,
    db: Session = Depends(get_db)
):
    return indexAll(accessUser=accessUser, filterModel=filterModel, db=db)


@router.post('/create', response_model=AuthUserModel, name="admn_auth_user_create", status_code=201)
def create(
    model: AuthUserCreateModel,
    accessUser: Annotated[AuthUser, Depends(auth_service2.getAccessUser)],
    db: Session = Depends(get_db)
):
    authRole_repo = RoleRepository(db)
    
    authRole = authRole_repo.findOneId(model.authRoleId)
    if not authRole:
        raise HTTPException(status_code=404, detail="AuthRole id not found")
    
    authUserModel = model.dict()
    authUserModel['password'] = '123'
    passwordPlain = authUserModel['password']
    passwordHash = auth_service2.passwordHash(passwordPlain)
    authUserModel['password'] = passwordHash
    
    authUser = AuthUser(**authUserModel)
    db.add(authUser)
    db.commit() 
    db.refresh(authUser)

    jsonResult = jsonable_encoder(authUser)
    return JSONResponse(jsonResult)


@router.put('/{id}/update', response_model=AuthUserModel, name="admn_auth_user_update")
def update(
    id: Annotated[int, Path(title="AuthUser id")],
    authUserUpdate: AuthUserUpdateModel,
    accessUser: Annotated[AuthUser, Depends(auth_service2.getAccessUser)], 
    db: Session = Depends(get_db)
):
    authUser_repo = UserRepository(db)
    authUser = authUser_repo.findOne(id)

    if not authUser:
        raise HTTPException(status_code=404, detail="AuthUser not found")

    authUser.firstname = authUserUpdate.firstname
    authUser.lastname = authUserUpdate.lastname
    authUser.email = authUserUpdate.email
    authUser.mobile = authUserUpdate.mobile
    authUser.authRoleId = authUserUpdate.authRoleId

    db.commit()
    db.refresh(authUser)

    jsonResult = jsonable_encoder(authUser)
    return JSONResponse(jsonResult)


@router.get('/{id}/detail', response_model = AuthUserModel, name = "admn_auth_user_detail")
def indexDetail(
    id: Annotated[int, Path(title="AuthUser id")],
    accessUser: Annotated[AuthUser, Depends(auth_service2.getAccessUser)],
    db: Session = Depends(get_db)
):
    authUser_repo = UserRepository(db)
    
    authUser = authUser_repo.findOne(id)
    if not authUser:
         raise HTTPException(status_code=404, detail="AuthUser id not found")
     
    return authUser


@router.get('/employee', name = "admn_auth_user_employee")
def indexEmployee(
    accessUser: Annotated[AuthUser, Depends(auth_service2.getAccessUser)],
    db: Session = Depends(get_db)
):
    authUser_repo = UserRepository(db)
    
    id = 2
    userEmployee = authUser_repo.findEmployee(id)
    
    employees = {}
    for item in userEmployee:
        employees[item.id] = item.email
    
    return employees

@router.get('/{email}/email', name = "admn_auth_user_role")
def indexRole(
    email: Annotated[str, Path(title="AuthUser email")],
    accessUser: Annotated[AuthUser, Depends(auth_service2.getAccessUser)],
    db: Session = Depends(get_db)
):
    authUser_repo = UserRepository(db)
    
    userEmployee = authUser_repo.findOneByEmail(email)
    
    return userEmployee


@router.delete('/{id}/delete', response_model=AuthUserModel, name="admn_auth_user_delete")
def delete(
    id: Annotated[int, Path(title="AuthUser id")],
    accessUser: Annotated[AuthUser, Depends(auth_service2.getAccessUser)],
    db: Session = Depends(get_db)
):
    authUser_repo = UserRepository(db)
    authUserDb: AuthUser = authUser_repo.findOne(id)
    if not authUserDb:
        raise HTTPException(status_code=404, detail="AuthUser not found")

    authUserDb.isDeleted = True
    db.commit()

    jsonResult = jsonable_encoder(authUserDb)
    return JSONResponse(jsonResult)