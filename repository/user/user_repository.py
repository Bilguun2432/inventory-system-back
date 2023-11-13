from datetime import datetime
from fastapi.encoders import jsonable_encoder
from sqlalchemy import and_, desc, or_, func, column
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.sql import select

# Schema
from schema.auth_module import AuthUser, AuthRole, AuthUserRole, AuthRolePermission, AuthUserPasswordReset
# Model
from model.modules.auth import models
from model.modules.auth.models import PaginationModel
from model.common import PaginateResponseModel, SortTypeEnum
from model.modules.auth.user_models import AuthUserListRequestModel, AuthUserPaginateResponseModel


class UserRepository:
    
    def __init__(self, db: Session):
        self.db = db

    def findAll(self, model: AuthUserPaginateResponseModel):
        qb =  self.db.query(AuthUser)\
            .options(joinedload(AuthUser.roles))\
            .filter(AuthUser.isDeleted != True)
            
        if not model:
            return qb.all()
        
        qb = qb.filter(and_(
                 AuthUser.firstname.ilike(f"%{model.filter.firstname if model.filter.firstname else ''}%"),
                 AuthUser.lastname.ilike(f"%{model.filter.lastname if model.filter.lastname else ''}%"),
                 AuthUser.userType.ilike(f"%{model.filter.userType if model.filter.userType else ''}%"),
                 AuthUser.email.ilike(f"%{model.filter.email if model.filter.email else ''}%"),
                 AuthUser.mobile.ilike(f"%{model.filter.mobile if model.filter.mobile else ''}%"),
             ))

        totalCount = qb.count()
        items = qb\
            .offset((model.pagination.page) * model.pagination.size)\
            .limit(model.pagination.size).all()

        return {
            "page": model.pagination.page,
            "size": model.pagination.size,
            "totalItems": totalCount,
            "items": items
        }
    
    def findFiltered(self, model: models.UserFilterModel ):
        qb =  self.db.query(AuthUser)\
            .options(joinedload(AuthUser.roles))\
            .filter(AuthUser.isDeleted == False)\
            .order_by(AuthUser.timeCreated.desc())
            
        if not model:
            return qb.all()
        
        qb = qb.filter(and_(
                 AuthUser.firstname.ilike(f"%{model.filterModel.firstname if model.filterModel.firstname else ''}%"),
                 AuthUser.lastname.ilike(f"%{model.filterModel.lastname if model.filterModel.lastname else ''}%"),
                 AuthUser.userType.ilike(f"%{model.filterModel.userType if model.filterModel.userType else ''}%"),
                 AuthUser.email.ilike(f"%{model.filterModel.email if model.filterModel.email else ''}%"),
                 AuthUser.mobile.ilike(f"%{model.filterModel.mobile if model.filterModel.mobile else ''}%"),
             ))

        return qb.all()

    def findOne(self, id: int):
        return self.db.query(AuthUser)\
            .options(joinedload(AuthUser.roles))\
            .filter(AuthUser.id == id).first()

    def findOneByEmail(self, email: str):
        return self.db.query(AuthUser)\
            .options(joinedload(AuthUser.roles))\
            .filter(AuthUser.email == email)\
            .first()

    def findOneByPassword(self, oldpassword: str):
        return self.db.query(AuthUser)\
            .options(joinedload(AuthUser.roles))\
            .filter(AuthUser.password == oldpassword).first()

    def getPaginateResult(self, listRequest: AuthUserListRequestModel):

        query = self.db.query(AuthUser)\
            .filter(AuthUser.isDeleted == False)
            
        filters = []

        if listRequest.filter.firstname:
            filters.append(AuthUser.firstname.ilike(f"%{listRequest.filter.firstname}%"))
        if listRequest.filter.lastname:
            filters.append(AuthUser.lastname.ilike(f"%{listRequest.filter.lastname}%"))
        if listRequest.filter.userType:
            filters.append(AuthUser.userType.ilike(f"%{listRequest.filter.userType}%"))
        if listRequest.filter.email:
            filters.append(AuthUser.email.ilike(f"%{listRequest.filter.email}%"))
        if listRequest.filter.mobile:
            filters.append(AuthUser.mobile.ilike(f"%{listRequest.filter.mobile}%"))

            
        if filters:
            query = query.filter(and_(*filters))
        
        totalCount = query.count()
        query = query.order_by(AuthUser.email.asc())

        if listRequest.sort.sortType == SortTypeEnum.asc:
            query = query.order_by(getattr(AuthUser, listRequest.sort.field))
        else:
            query = query.order_by(desc(getattr(AuthUser, listRequest.sort.field)))


        offset = (listRequest.pagination.page) * listRequest.pagination.size
        query = query.limit(listRequest.pagination.size).offset(offset)

        items = query.all()

        itemResult = [item for item in items]

        resultDict = {
            "page": listRequest.pagination.page,
            "size": listRequest.pagination.size,
            "totalItems": totalCount,
            "items": itemResult
        }

        return resultDict

    def get_all(self,
                columns: str = None,
                sort: str = None,
                model: models.UserFilterModel = None
                ):
        
        page = model.pagination.page
        limit = model.pagination.limit
        
        query = self.db.query(AuthUser)

        filter_count = 0
        if columns is not None and columns != "all":
            query = select(AuthUser, columns=convert_sort(columns))
        if model is not None and model != "null":

            query = query.filter(and_(
                AuthUser.firstname.ilike(
                    f"%{model.filterModel.firstname if model.filterModel.firstname else ''}%"),
                AuthUser.lastname.ilike(
                    f"%{model.filterModel.lastname if model.filterModel.lastname else ''}%"),
                AuthUser.userType.ilike(
                    f"%{model.filterModel.userType if model.filterModel.userType else ''}%"),
                AuthUser.email.ilike(
                    f"%{model.filterModel.email if model.filterModel.email else ''}%"),
                AuthUser.mobile.ilike(
                    f"%{model.filterModel.mobile if model.filterModel.mobile else ''}%"),
            ))
            filter_count = query.count()

        count_query = select(func.count(1)).select_from(AuthUser)

        offset_page = page

        query = query.offset(offset_page * limit).limit(limit).all()

        total_record = (self.db.execute(count_query)).scalar() or 0

        result = jsonable_encoder(query)

        return PaginationModel(
            total_record=total_record,
            filter_count=filter_count,
            content=result
        )
    

def convert_sort(sort):
    """
    # separate string using split('-')
    split_sort = sort.split('-')
    # join to list with ','
    new_sort = ','.join(split_sort)
    """
    return ','.join(sort.split('-'))

    
def convert_columns(columns):
    """
    # seperate string using split ('-')
    new_columns = columns.split('-')

    # add to list with column format
    column_list = []
    for data in new_columns:
        column_list.append(data)

    # we use lambda function to make code simple

    """

    return list(map(lambda x: column(x), columns.split('-')))


class RoleRepository:
    def __init__(self, db: Session):
        self.db = db
    def findOneId(self, id: int):
        return self.db.query(AuthRole)\
        .options(joinedload(AuthRole.permissions))\
            .filter(AuthRole.id == id).first()
    def findOne(self, group_name: str):
        return self.db.query(AuthRole)\
            .filter(AuthRole.name == group_name).first()
    def findAll(self): 
        return self.db.query(AuthRole).all()


class UserRoleRepository:
    def __init__(self, db: Session):
        self.db = db
    def findAll(self): 
        return self.db.query(AuthUserRole).all()
    def findUserAndRole(self, user: int, role: int): 
        return self.db.query(AuthUserRole)\
            .filter(AuthUserRole.userId == user).filter(AuthUserRole.roleId == role).first()


class AuthRolePermissionRepository:
    def __init__(self, db: Session):
        self.db = db
    def findAll(self): 
        return self.db.query(AuthRolePermission).all()
    def findRoleAndPermission(self, role: int, permission: int): 
        return self.db.query(AuthRolePermission)\
            .filter(AuthRolePermission.roleId == role).filter(AuthRolePermission.permissionId == permission).first()


class AuthUserPasswordResetRepository:
    def __init__(self, db: Session):
        self.db = db

    def findAll(self):
        return self.db.query(AuthUserPasswordReset)\
            .options(joinedload(AuthUserPasswordReset.roles)).all()

    def findOneId(self, id: int):
        return self.db.query(AuthUserPasswordReset)\
            .filter(AuthUserPasswordReset.userId == id).first()
    
    def findOneByEmail(self, userId: int):
        return self.db.query(AuthUser)\
            .filter(AuthUser.id == userId).first()
    
    def create(self, data: dict):
        reset_request = AuthUserPasswordReset(**data)
        self.db.add(reset_request)
        self.db.commit()
        self.db.refresh(reset_request)
        return reset_request
    
    def find_one_by_active_token(self, reset_token: str):
        return self.db.query(AuthUserPasswordReset)\
            .filter(AuthUserPasswordReset.token == reset_token)\
            .filter(AuthUserPasswordReset.timeExpire > datetime.now())\
            .first()