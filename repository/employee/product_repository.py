from datetime import datetime
from fastapi.encoders import jsonable_encoder
from sqlalchemy import and_, desc, or_, func, column
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.sql import select

# Schema
from schema.action_module import ActionStatus, Action
from schema.product_module import AuthUserProduct
from schema.product_module import Product
# Model
from model.common import PaginateResponseModel, SortTypeEnum
from model.modules.employee.product_models import EmployeeProductPaginateResponseModel, EmployeeProductListRequestModel


class EmployeeProductRepository:
    
    def __init__(self, db: Session):
        self.db = db

    def findProducts(self, model: EmployeeProductPaginateResponseModel, id: int):
        qb = self.db.query(AuthUserProduct)\
            .options(joinedload(AuthUserProduct.product).joinedload(Product.category))\
            .filter(AuthUserProduct.unit != 0)\
            .filter(AuthUserProduct.userId == id)
                
        if not model:
            return qb.all()
        
        qb = qb.filter(and_(
                 AuthUserProduct.unit.ilike(f"%{model.filter.unit if model.filter.unit else ''}%"),
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

    def findOne(self, id: int):
        return self.db.query(AuthUserProduct)\
            .filter(AuthUserProduct.id == id).first()
            
    def findEmployee(self, id = int):
        return self.db.query(AuthUserProduct)\
            .filter(AuthUserProduct.authRoleId == id)\
            .all()

    def findOneByEmail(self, email: str):
        return self.db.query(AuthUserProduct)\
            .filter(AuthUserProduct.email == email)\
            .first()