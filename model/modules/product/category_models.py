from typing import List
from typing import Optional
from pydantic import BaseModel, root_validator
from datetime import datetime

# Model
from model.common import PaginateRequestModel, SortModel


# ========= ProductCategory Models ===========


class ProductCategoryModel(BaseModel):
    id: int
    name: str
    description: str
    enabled: bool = True
    isDeleted: bool = False
    userCreatedId: Optional[int]
    timeCreated: Optional[datetime]
    

class ProductCategoryCreateModel(BaseModel):
    name: str
    description: str
    

class ProductCategoryFilterModel(BaseModel):
    name: Optional[str] | None = None
    description: Optional[str] | None = None


class ProductCategoryListRequestModel(BaseModel):
    filter: ProductCategoryFilterModel
    sort: SortModel
    pagination: PaginateRequestModel
    
    
class ProductCategoryPaginateResponseModel(BaseModel):
    filter: ProductCategoryFilterModel
    sort: SortModel
    pagination: PaginateRequestModel
