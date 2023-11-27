from sqlalchemy import and_
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import asc

# Schema
from schema.product_module import Product, AuthUserProduct
# Model
from model.modules.product import models


class ProductRepository:
    
    def __init__(self, db: Session):
        self.db = db

    def findAll(self, model: models.ProductPaginateResponseModel):
        qb =  self.db.query(Product)\
            .options(joinedload(Product.category))\
            .filter(Product.isDeleted != True)
            
        if not model:
            return qb.all()
        
        qb = qb.filter(and_(
                 Product.name.ilike(f"%{model.filter.name if model.filter.name else ''}%"),
                 Product.description.ilike(f"%{model.filter.description if model.filter.description else ''}%"),
             ))
        totalCount = qb.count()

        items = qb\
            .order_by(asc(Product.id))\
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
            .options(joinedload(Product.category))\
            .filter(Product.id == id)\
            .first()
    
    def findOneCategoryIdFilter(self, model: models.ProductPaginateResponseModel, categoryId: int):
        qb =  self.db.query(Product)\
            .filter(Product.categoryId == categoryId)

        if not model:
            return qb.all()
        
        qb = qb.filter(and_(
                 Product.name.ilike(f"%{model.filter.name if model.filter.name else ''}%"),
                 Product.description.ilike(f"%{model.filter.description if model.filter.description else ''}%"),
             ))
        totalCount = qb.count()

        items = qb\
            .order_by(asc(Product.id))\
            .offset((model.pagination.page) * model.pagination.size)\
            .limit(model.pagination.size).all()

        return {
            "page": model.pagination.page,
            "size": model.pagination.size,
            "totalItems": totalCount,
            "items": items
        }
        
    def findOneCategoryId(self, categoryId: int):
        return self.db.query(Product)\
            .filter(Product.categoryId == categoryId)\
            .all()
            

class AuthUserProductRepository:
    
    def __init__(self, db: Session):
        self.db = db

    def findAll(self):
        return self.db.query(AuthUserProduct)\
            .all()
    
    def findOneName(self, id: int, name: str):
        return self.db.query(AuthUserProduct)\
            .filter(and_(AuthUserProduct.categoryId == id, Product.name == name))\
            .first()
            
    def findAuthUserProduct(self, productId: int, authUserId: int):
        return self.db.query(AuthUserProduct)\
            .filter(AuthUserProduct.productId == productId)\
            .filter(AuthUserProduct.userId == authUserId)\
            .first()
    
    def findOneCategoryId(self, categoryId: int):
        return self.db.query(AuthUserProduct)\
            .filter(AuthUserProduct.categoryId == categoryId)\
            .all()