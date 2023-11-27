from datetime import datetime
from fastapi.encoders import jsonable_encoder
from sqlalchemy import and_, desc, or_, func, column
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.sql import select

# Schema
from schema.action_module import ActionStatus

class ActionStatusRepository:
    
    def __init__(self, db: Session):
        self.db = db

    def findAll(self):
        return self.db.query(ActionStatus)\
            .all()