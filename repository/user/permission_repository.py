from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, desc

# Schema
from schema.auth_module import AuthPermission
# Model
from model.modules.auth.permission_models import AuthPermissionListRequestModel, AuthPermissionPaginateResponseModel
from model.common import SortTypeEnum


class PermissionRepository:
    
    def __init__(self, db: Session):
        self.db = db
        
    def findOneId(self, id: int):
        return self.db.query(AuthPermission)\
            .filter(AuthPermission.id == id)\
            .first()
            
    def findOne(self, group_name: str):
        return self.db.query(AuthPermission)\
            .filter(AuthPermission.permissionKey == group_name)\
            .first()
            
    def findAll(self, model: AuthPermissionPaginateResponseModel):
        qb =  self.db.query(AuthPermission).filter()
            
        if not model:
            return qb.all()
        
        qb = qb.filter(and_(
                 AuthPermission.name.ilike(f"%{model.filter.name if model.filter.name else ''}%"),
                 AuthPermission.permissionKey.ilike(f"%{model.filter.permissionKey if model.filter.permissionKey else ''}%"),
                 AuthPermission.group_name.ilike(f"%{model.filter.group_name if model.filter.group_name else ''}%"),
                 AuthPermission.description.ilike(f"%{model.filter.description if model.filter.description else ''}%"),
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
    
    def getPaginateResult(self, listRequest: AuthPermissionListRequestModel):
        query = self.db.query(AuthPermission)\
            .distinct()
            
        filters = []

        if listRequest.filter.name:
            filters.append(AuthPermission.name.ilike(f"%{listRequest.filter.name}%"))
        if listRequest.filter.group_name:
            filters.append(AuthPermission.group_name.ilike(f"%{listRequest.filter.group_name}%"))
        if listRequest.filter.permissionKey:
            filters.append(AuthPermission.permissionKey.ilike(f"%{listRequest.filter.permissionKey}%"))
        if listRequest.filter.description:
            filters.append(AuthPermission.description.ilike(f"%{listRequest.filter.description}%"))

            
        if filters:
            query = query.filter(and_(*filters))
        
        totalCount = query.count()

        if listRequest.sort.sortType == SortTypeEnum.asc:
            query = query.order_by(getattr(AuthPermission, listRequest.sort.field))
        else:
            query = query.order_by(desc(getattr(AuthPermission, listRequest.sort.field)))


        offset = (listRequest.pagination.page) * listRequest.pagination.size
        query = query.limit(listRequest.pagination.size).offset(offset)

        items = query.all()

        resultDict = {
            "page": listRequest.pagination.page,
            "size": listRequest.pagination.size,
            "totalItems": totalCount,
            "items": items
        }

        return resultDict