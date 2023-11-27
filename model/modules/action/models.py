from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, root_validator


class ActionModel(BaseModel):
    id: int
    status: str