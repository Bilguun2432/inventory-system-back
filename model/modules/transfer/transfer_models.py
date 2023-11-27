from typing import List
from typing import Optional
from pydantic import BaseModel, root_validator
from datetime import datetime

# ========= Transfer Models ===========


class TransferModel(BaseModel):
    email: str
    productId: int
    transferUnit: int