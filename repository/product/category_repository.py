from sqlalchemy import and_, desc
from sqlalchemy.orm import Session, joinedload

# Schema
from schema.product_module import ProductCategory
# Model
from model.common import SortTypeEnum
from model.modules.product.category_models import ProductCategoryListRequestModel, ProductCategoryPaginateResponseModel


class ProductCategoryRepository:
    
    def __init__(self, db: Session):
        self.db = db
        
    def findAll(self, model: ProductCategoryPaginateResponseModel):
        qb =  self.db.query(ProductCategory)\
            .filter(ProductCategory.isDeleted != True)
            
        if not model:
            return qb.all()
        
        qb = qb.filter(and_(
                 ProductCategory.name.ilike(f"%{model.filter.name if model.filter.name else ''}%"),
                 ProductCategory.description.ilike(f"%{model.filter.description if model.filter.description else ''}%"),
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

    def findOneId(self, id: int):
        return self.db.query(ProductCategory)\
            .filter(ProductCategory.id == id)\
            .first()
        
    def findOneName(self, name: str):
        return self.db.query(ProductCategory)\
            .filter(ProductCategory.name == name).first()
            
    def find(self):
        return self.db.query(ProductCategory)\
            .all()