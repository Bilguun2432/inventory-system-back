from typing import List
from typing import Optional
from pydantic import BaseModel, root_validator
from datetime import datetime


# ========= ProductCategory Models ===========


class AuthUserProductModel(BaseModel):
    id: int
    userId: int
    productId: int
    unit: int
    timeCreated: datetime