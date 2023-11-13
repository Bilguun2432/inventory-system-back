from typing import Annotated
from fastapi import Depends, HTTPException, APIRouter, Path
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from config.database import get_db

# Lib
from lib import auth_service2, http
# Model
from model.modules.product.category_models import ProductCategoryModel, ProductCategoryCreateModel, \
    ProductCategoryFilterModel, ProductCategoryListRequestModel, ProductCategoryPaginateResponseModel
from model.common import PaginateResponseModel
# Repo
from repository.product.category_repository import ProductCategoryRepository
# Schema
from schema.auth_module import AuthUser
from schema.product_module import ProductCategory

router = APIRouter(
    prefix="/product/category",
    tags=["ProductCategory"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


def indexAll(
    accessUser: Annotated[AuthUser, Depends(auth_service2.getAccessUser)],
    filterModel: ProductCategoryPaginateResponseModel = None,
    db: Session = Depends(get_db)
):
    productCategory_repo = ProductCategoryRepository(db)
    productCategorys = productCategory_repo.findAll(model=filterModel)
    return http.successResponse(data = productCategorys)


@router.get('/', response_model = list[ProductCategoryModel], name = "admn_product_category_index")
def getAll (
    accessUser: Annotated[AuthUser, Depends(auth_service2.getAccessUser)],
    filterModel: ProductCategoryPaginateResponseModel = None,
    db: Session = Depends(get_db)
):
    return indexAll(accessUser=accessUser, filterModel=filterModel, db=db)


@router.post("/", response_model = list[ProductCategoryModel], name = "admn_product_category_index")
def postIndex(
    accessUser: Annotated[AuthUser, Depends(auth_service2.getAccessUser)],
    filterModel: ProductCategoryPaginateResponseModel,
    db: Session = Depends(get_db)
):
    return indexAll(accessUser=accessUser, filterModel=filterModel, db=db)


@router.post('/create', response_model=ProductCategoryModel, name="admn_product_category_create", status_code=201)
def create(
    createModel: ProductCategoryCreateModel, 
    accessUser: Annotated[AuthUser, Depends(auth_service2.getAccessUser)],
    db: Session = Depends(get_db)
):
    productCategory_repo = ProductCategoryRepository(db)
    
    productCategory = productCategory_repo.findOneName(name = createModel.name)
    if productCategory:
        raise HTTPException(status_code=400, detail="Product category already exists")
    
    productCategoryCreateData = createModel.dict()
    productCategoryCreateData['userCreatedId'] = accessUser.id
    productCategoryCreated = ProductCategory(**productCategoryCreateData)
    db.add(productCategoryCreated)

    db.commit()
    db.refresh(productCategoryCreated)

    result = jsonable_encoder(productCategoryCreated)

    return JSONResponse(result)


@router.put('/{id}/update', response_model=ProductCategoryModel, name="admn_product_category_update")
def update(
    id: Annotated[int, Path(title="ProductCategory id")],
    updateModel: ProductCategoryCreateModel, 
    accessUser: Annotated[AuthUser, Depends(auth_service2.getAccessUser)],
    db: Session = Depends(get_db)
):
    productCategory_repo = ProductCategoryRepository(db)
    productCategoryDb = productCategory_repo.findOneId(id)
    if not productCategoryDb:
        raise HTTPException(status_code=404, detail="ProductCategory not found")

    productCategoryDb.name = updateModel.name
    productCategoryDb.description = updateModel.description

    db.commit()
    db.refresh(productCategoryDb)    
    
    result = jsonable_encoder(productCategoryDb)

    return JSONResponse(result)


@router.get('/{id}/detail', response_model=ProductCategoryModel, name="admn_product_category_detail")
def detail(
    id: Annotated[int, Path(title="ProductCategory id")],
    accessUser: Annotated[AuthUser, Depends(auth_service2.getAccessUser)],
    db: Session = Depends(get_db)
):
    productCategory = ProductCategoryRepository(db).findOneId(id)
    if not productCategory:
        raise HTTPException(status_code=404, detail="ProductCategory not found")
    
    jsonResult = jsonable_encoder(productCategory)
    return JSONResponse(jsonResult)


# @router.delete('/{id}/delete', response_model=ProductCategoryModel, name="admn_product_category_delete")
# def delete(
#     id: Annotated[int, Path(title="ProductCategory id")],
#     accessUser: Annotated[AuthUser, Depends(auth_service2.getAccessUser)],
#     db: Session = Depends(get_db)
# ):
#     repo = ProductCategoryRepository(db)
#     productCategoryDb = repo.find(id)
#     if not productCategoryDb:
#         raise HTTPException(status_code=404, detail="ProductCategory not found")
    
#     productCategoryDb.isDeleted = True
#     db.commit()
#     db.refresh(productCategoryDb)

#     jsonResult = jsonable_encoder(productCategoryDb)
#     return JSONResponse(jsonResult)