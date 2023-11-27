from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, root_validator

# Model
from model.common import PaginateRequestModel, SortModel
from model.modules.product.models import ProductModel

class AuthUserProductModel(BaseModel):
    id: int
    userId: int
    productId: int
    unit: int
    timeCreated: datetime
    
    product: ProductModel
    

class AuthUserTransferProductModel(BaseModel):
    actionStatusId: int
    authUserId: int
    transferUnit: int
    description: Optional[str]
    
    authUserProduct: AuthUserProductModel


class EmployeeProductFilterModel(BaseModel):
    unit: Optional[int] | None = None


class EmployeeProductListRequestModel(BaseModel):
    filter: EmployeeProductFilterModel
    sort: SortModel
    pagination: PaginateRequestModel


class EmployeeProductPaginateResponseModel(BaseModel):
    filter: EmployeeProductFilterModel
    sort: SortModel
    pagination: PaginateRequestModel
    
class EmployeeProductMailModel(BaseModel):
    email: str