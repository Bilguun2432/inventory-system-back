from datetime import datetime
from typing import Optional, Union
from pydantic import BaseModel, ConfigDict
from fastapi import UploadFile, File

# Model
from model.common import PaginateRequestModel, SortModel
from model.modules.product.category_models import ProductCategoryModel


class ProductModel(BaseModel):
    id: int
    categoryId: Optional[int]
    name: str
    price: Optional[int]
    unit: int
    description: Optional[str]
    userCreatedId: int | None = None
    enabled: bool
    isDeleted: bool
    timeCreated: datetime
    imagePath: Optional[str]
    
    category: ProductCategoryModel


class ProductCreateModel(BaseModel):
    category: str
    name: str
    description: Optional[str] | None = None 
    price:  int
    unit: int
    enabled: Optional[bool] | None = None
    
class ProductUpdateModel(BaseModel):
    name: str
    description: Optional[str] | None = None
    price:  int
    unit: int
    enabled: Optional[bool] | None = None


class ProductFilterModel(BaseModel):
    name: Optional[str] | None = None
    description: Optional[str] | None = None
    priceMin: Optional[int] | None = None
    priceMax: Optional[int] | None = None

class PaginationModel(BaseModel):
    pagenumber: Optional[int] | None = None
    count: Optional[int] | None =  None

class ProductPaginateResponseModel(BaseModel):
    filter: ProductFilterModel
    sort: SortModel
    pagination: PaginateRequestModel
