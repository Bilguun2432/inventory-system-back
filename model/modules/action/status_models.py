from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, root_validator
from model.modules.product.models import ProductModel


class ActionStatusModel(BaseModel):
    id: int
    actionStatusId: int
    authUserId: int
    productId: int
    unit: int
    description: str
    timeCreated: datetime

    product: Optional[ProductModel]

class ActionEmployeeModel(BaseModel):
    id: int