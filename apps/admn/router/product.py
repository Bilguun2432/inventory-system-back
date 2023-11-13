from datetime import datetime
from typing import Annotated, List
from fastapi import Depends, HTTPException, APIRouter, Path, Query
from sqlalchemy.orm import Session
from config.database import get_db
from googletrans import Translator

# Lib
from lib import auth_service2, http
# Model
from model.modules.product.models import ProductModel, ProductPaginateResponseModel, ProductCreateModel
# Repo
from repository.product.repository import ProductRepository
from repository.product.category_repository import ProductCategoryRepository
# Schema
from schema.auth_module import AuthUser
from schema.product_module import Product


router = APIRouter(
    prefix="/product",
    tags=["Product"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


def indexAll(
    accessUser: Annotated[AuthUser, Depends(auth_service2.getAccessUser)],
    filterModel: ProductPaginateResponseModel = None,
    db: Session = Depends(get_db)
):
    repo = ProductRepository(db)
    products = repo.findAll(model=filterModel)
    return http.successResponse(data = products)


@router.get('/', response_model=List[ProductModel] , name="admn_product_index")
def getIndex (
    accessUser: Annotated[AuthUser, Depends(auth_service2.getAccessUser)],
    filterModel: ProductPaginateResponseModel = None,
    db: Session = Depends(get_db)
):
    return indexAll(accessUser=accessUser, filterModel=filterModel, db=db)


@router.post('/', response_model=List[ProductModel], name="admn_product_index")
def postIndex (
    accessUser: Annotated[AuthUser, Depends(auth_service2.getAccessUser)],
    filterModel: ProductPaginateResponseModel,
    db: Session = Depends(get_db)
):
    return indexAll(accessUser=accessUser, filterModel=filterModel, db=db)


@router.post('/create', response_model=ProductModel, name="admn_product_create", status_code=201)
def create(
    createModel: ProductCreateModel,
    accessUser: Annotated[AuthUser, Depends(auth_service2.getAccessUser)],
    db: Session = Depends(get_db)
):
    productCategory_repo = ProductCategoryRepository(db)
    product_repo = ProductRepository(db)
    
    categoryId = createModel.categoryId
    productCategory = productCategory_repo.findOneId(categoryId)
    if not productCategory:
        return http.notFoundResponse(message="ProductCategory not found")

    product = product_repo.findOneName(id = productCategory.id, name = createModel.name)
    if product:
        raise HTTPException(status_code=400, detail="Product already exists")

    productCreated = Product(**createModel.__dict__)
    productCreated.userCreatedId = accessUser.id

    db.add(productCreated)
    db.commit()
    db.refresh(productCreated)

    productModel = ProductModel(**productCreated.__dict__)

    return http.createdResponse(data=productModel)


@router.get('/{id}/detail', response_model=ProductModel, name="admn_product_detail")
def detail (
    accessUser: Annotated[AuthUser, Depends(auth_service2.getAccessUser)],
    id: Annotated[int, Path(title="Product ID")],
    db: Session = Depends(get_db)
):
    repo = ProductRepository(db)
    product = repo.find(id)

    if not product:
        return http.notFoundResponse(message="Product not found")

    return http.successResponse(data = product)


@router.put('/{id}/update', response_model=ProductModel, name="admn_product_update")
def update(
    id: Annotated[int, Path(title="Product id")],
    updateModel: ProductCreateModel,
    accessUser: Annotated[AuthUser, Depends(auth_service2.getAccessUser)],
    db: Session = Depends(get_db)
):
    repo = ProductRepository(db)
    productDb = repo.find(id)
    if not productDb:
        return http.notFoundResponse("Product not found")

    categoryId = updateModel.categoryId
    categoryRepo = ProductCategoryRepository(db)
    category = categoryRepo.find(categoryId)

    if not category:
        return http.notFoundResponse("ProductCategory not found")

    updateData = updateModel.model_dump()
    for key, value in updateData.items():
        setattr(productDb, key, value)

    translate = repo.findTranslate(productDb.id, 'mn')
    if not translate:
        translate = ProductTranslate(
            product = productDb,
            lang = "mn",
            name = productDb.name,
            description = productDb.description
        )
        db.add(translate)

    translate.name = productDb.name
    translate.description = productDb.description

    db.add(productDb)
    db.commit()
    db.refresh(productDb)

    productModel = ProductModel(**productDb.__dict__)

    return http.successResponse(data=productModel)



@router.delete('/{id}/delete', response_model=ProductModel, name="admn_product_delete")
def delete(
    id: Annotated[int, Path(title="Product id")],
    accessUser: Annotated[AuthUser, Depends(auth_service2.getAccessUser)],
    db: Session = Depends(get_db)
):
    repo = ProductRepository(db)
    productDb = repo.find(id)
    if not productDb:
        return http.notFoundResponse("Product not found")

    productDb.isDeleted = True
    db.commit()
    db.refresh(productDb)

    productModel = ProductModel(**productDb.__dict__)
    return http.successResponse(data=productModel, message="Product deleted")


@router.get('/filter', name="admn_product_filter", status_code=201)
def create(
    # accessUser: Annotated[AuthUser, Depends(auth_service2.getAccessUser)],
    db: Session = Depends(get_db),
    pricemin: float = Query(None),
    pricemax: float = Query(None),
    name: str = Query(None),
    description: str = Query(None),
):
    products = ProductRepository(db).filter(name, description, pricemin, pricemax)
    # print(jsonable_encoder(products))
    return products

