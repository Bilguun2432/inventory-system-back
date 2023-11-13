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
from model.modules.auth.role_models import AuthRoleAddModel
from model.modules.auth.user_models import AuthUserCreateModel, AuthUserUpdateModel, AuthUserModel, AuthUserRoleModel
from model.modules.auth.user_models import AuthUserListRequestModel, AuthUserPaginateResponseModel
# Repo
from repository.user.user_repository import UserRepository, RoleRepository, UserRoleRepository
# Schema
from schema.auth_module import AuthUser, AuthUserRole


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


@router.get('/{id}', response_model = AuthUserModel, name = "admn_auth_user_detail")
def indexDetail(
    id: Annotated[int, Path(title="AuthUser id")],
    accessUser: Annotated[AuthUser, Depends(auth_service2.getAccessUser)],
    db: Session = Depends(get_db)
):
    repo = UserRepository(db).findOne(id)
    if not repo:
         raise HTTPException(status_code=404, detail="AuthUser id not found")
    return repo


@router.post('/create', response_model=AuthUserModel, name="admn_auth_user_create", status_code=201)
def create(
    authUserCreate: AuthUserCreateModel,
    # accessUser: Annotated[AuthUser, Depends(auth_service2.getAccessUser)],
    db: Session = Depends(get_db)
):
    createObj = authUserCreate.dict()
    createObj['password'] = '123'
    passwordPlain = createObj['password']
    passwordHash = auth_service2.passwordHash(passwordPlain)
    createObj['password'] = passwordHash
    authUser = AuthUser(**createObj)
    print(jsonable_encoder(authUser))
    db.add(authUser)
    db.commit() 
    db.refresh(authUser)

    # result = AuthUserModel(**authUser.__dict__)
    
    # return result
    jsonResult = jsonable_encoder(authUser)
    return JSONResponse(jsonResult)


@router.put('/{id}/update', response_model=AuthUserModel, name="admn_auth_user_update")
def update(
    id: Annotated[int, Path(title="AuthUser id")],
    authUserUpdate: AuthUserUpdateModel,
    accessUser: Annotated[AuthUser, Depends(auth_service2.getAccessUser)], 
    db: Session = Depends(get_db)
):
    repo = UserRepository(db)
    authUserDb = repo.findOne(id)

    if not authUserDb:
        raise HTTPException(status_code=404, detail="AuthUser not found")

    authUserDb.firstname = authUserUpdate.firstname
    authUserDb.lastname = authUserUpdate.lastname
    authUserDb.email = authUserUpdate.email
    authUserDb.mobile = authUserUpdate.mobile
    authUserDb.userType = authUserUpdate.userType

    db.commit()
    db.refresh(authUserDb)

    jsonResult = jsonable_encoder(authUserDb)
    return JSONResponse(jsonResult)


@router.delete('/{id}/delete', response_model=AuthUserModel, name="admn_auth_user_delete")
def delete(
    id: Annotated[int, Path(title="AuthUser id")],
    accessUser: Annotated[AuthUser, Depends(auth_service2.getAccessUser)],
    db: Session = Depends(get_db)
):
    repo = UserRepository(db)
    authUserDb: AuthUser = repo.findOne(id)
    if not authUserDb:
        raise HTTPException(status_code=404, detail="AuthUser not found")

    authUserDb.isDeleted = True
    db.commit()

    jsonResult = jsonable_encoder(authUserDb)
    return JSONResponse(jsonResult)


@router.post('/{id}/role/add', response_model=AuthUserRoleModel, name="admn_auth_user_addRole", status_code=201)
def addRole(
    id: Annotated[int, Path(title="AuthRole id")],
    model: AuthRoleAddModel,
    accessUser: Annotated[AuthUser, Depends(auth_service2.getAccessUser)],
    db: Session = Depends(get_db)
):
    if(not UserRepository(db).findOne(id)):
        raise HTTPException(status_code=404, detail="AuthUser not exist")
    if(not RoleRepository(db).findOneId(model.roleId)):
        raise HTTPException(status_code=404, detail="Role id not exist")
    if UserRoleRepository(db).findUserAndRole(id, model.roleId):
        raise HTTPException(status_code=404, detail="UserRole already exist")
    authRole = AuthUserRole(userId=id, roleId=model.roleId)
    db.add(authRole)
    db.commit()
    db.refresh(authRole)
    return authRole


@router.delete('/{id}/role/{roleId}/remove', response_model=AuthUserRoleModel, name="admn_auth_user_deleteRole")
def deleteRole(
    id: Annotated[int, Path(title="AuthRole id")],
    roleId: Annotated[int, Path(title="AuthRole id")],
    accessUser: Annotated[AuthUser, Depends(auth_service2.getAccessUser)],
    db: Session = Depends(get_db)
):
    userRole =  UserRoleRepository(db).findUserAndRole(id, roleId)
    if(not userRole):
        raise HTTPException(status_code=404, detail="UserRole not exist exist")
    db.delete(userRole)
    db.commit()
    return userRole