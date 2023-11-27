from sqlalchemy import and_, desc
from sqlalchemy.orm import Session, joinedload

# Schema
from schema.action_module import ActionStatus, Action
# Model
from model.common import SortTypeEnum
from model.modules.product.category_models import ProductCategoryListRequestModel, ProductCategoryPaginateResponseModel


class TransferRepository:
    
    def __init__(self, db: Session):
        self.db = db

    def findOneId(self, id: int):
        return self.db.query(ActionStatus)\
            .filter(ActionStatus.id == id)\
            .first()
        
    def findOneName(self, name: str):
        return self.db.query(ActionStatus)\
            .filter(ActionStatus.name == name).first()
            
    def find(self):
        return self.db.query(ActionStatus)\
            .all()