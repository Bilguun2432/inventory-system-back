from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

# Model
from model.common import PaginateRequestModel, SortModel


class ProductModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    categoryId: Optional[int]
    name: str
    price: Optional[int]
    unit: int
    description: Optional[str]
    packageCode: Optional[str] | None = None
    productCompletionId: int | None = None
    userCreatedId: int | None = None
    enabled: bool
    isDeleted: bool
    timeCreated: datetime


class ProductCreateModel(BaseModel):
    category: str
    name: str
    description: Optional[str] | None = None
    price:  Optional[int] = None
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
