from datetime import datetime
from fastapi.encoders import jsonable_encoder
from sqlalchemy import and_, desc, or_, func, column
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.sql import select

# Schema
from schema.action_module import Action


class ActionRepository:
    
    def __init__(self, db: Session):
        self.db = db
    
    def findAll(self):
        return self.db.query(Action)\
            .all()
    
    def findSoldAdmin(self):
        return self.db.query(Action)\
            .filter(Action.actionStatusId == 2)\
            .all()
    
    def findSoldEmployee(self, id: int):
        return self.db.query(Action)\
            .options(joinedload(Action.Product))\
            .filter(Action.authUserId == id)\
            .filter(Action.actionStatusId == 2)\
            .all()
    
    def findBrokenEmployee(self, id: int):
        return self.db.query(Action)\
            .options(joinedload(Action.Product))\
            .filter(Action.authUserId == id)\
            .filter(Action.actionStatusId == 1)\
            .all()
    
    def findReturnedEmployee(self, id: int):
        return self.db.query(Action)\
            .options(joinedload(Action.Product))\
            .filter(Action.authUserId == id)\
            .filter(Action.actionStatusId == 3)\
            .all()
    
    def findArchive(self):
        return self.db.query(Action)\
            .options(joinedload(Action.Product))\
            .all()