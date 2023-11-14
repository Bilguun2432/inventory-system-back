from sqlalchemy import and_
from sqlalchemy.orm import Session, joinedload

# Schema
from schema.product_module import Product
# Model
from model.modules.product import models


class ProductRepository:
    
    def __init__(self, db: Session):
        self.db = db

    def findAll(self, model: models.ProductPaginateResponseModel ):
        qb =  self.db.query(Product)\
            .filter(Product.isDeleted != True)
            
        if not model:
            return qb.all()
        
        qb = qb.filter(and_(
                 Product.name.ilike(f"%{model.filter.name if model.filter.name else ''}%"),
                 Product.description.ilike(f"%{model.filter.description if model.filter.description else ''}%"),
             ))
        totalCount = qb.count()

        items = qb\
            .order_by(Product.id.desc())\
            .offset((model.pagination.page) * model.pagination.size)\
            .limit(model.pagination.size).all()

        return {
            "page": model.pagination.page,
            "size": model.pagination.size,
            "totalItems": totalCount,
            "items": items
        }
    
    def findOneName(self, id: int, name: str):
        return self.db.query(Product)\
            .filter(and_(Product.categoryId == id, Product.name == name))\
            .first()
            
    def findOneId(self, id: int):
        return self.db.query(Product)\
            .filter(Product.id == id)\
            .first()
    
    def findOneCategoryId(self, categoryId: int):
        return self.db.query(Product)\
            .filter(Product.categoryId == categoryId)\
            .all()