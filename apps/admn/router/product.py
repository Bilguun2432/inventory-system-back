from datetime import datetime
from typing import Annotated, List
from fastapi import Depends, HTTPException, APIRouter, Path, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from config.database import get_db
from fastapi import File, UploadFile
import os, datetime
from fastapi import Form, File, UploadFile
from fastapi.responses import FileResponse


# Lib
from lib import auth_service2, http
# Model
from model.modules.product.models import ProductModel, ProductPaginateResponseModel, ProductCreateModel, ProductUpdateModel
# Repo
from repository.product.repository import ProductRepository
from repository.product.category_repository import ProductCategoryRepository
# Schema
from schema.auth_module import AuthUser
from schema.product_module import Product
from fastapi import FastAPI, Form


router = APIRouter(
    tags=["Product"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


def indexAll(
    accessUser: Annotated[AuthUser, Depends(auth_service2.getAccessUser)],
    filterModel: ProductPaginateResponseModel = None,
    db: Session = Depends(get_db)
):
    product_repo = ProductRepository(db)
    products = product_repo.findAll(model=filterModel)
    
    return http.successResponse(data = products)


@router.get('/product', response_model=List[ProductModel], name="admn_product_index")
def getIndex (
    accessUser: Annotated[AuthUser, Depends(auth_service2.getAccessUser)],
    filterModel: ProductPaginateResponseModel = None,
    db: Session = Depends(get_db)
):
    return indexAll(accessUser=accessUser, filterModel=filterModel, db=db)


@router.post('/product', response_model=List[ProductModel], name="admn_product_index")
def postIndex (
    accessUser: Annotated[AuthUser, Depends(auth_service2.getAccessUser)],
    filterModel: ProductPaginateResponseModel,
    db: Session = Depends(get_db)
):
    return indexAll(accessUser=accessUser, filterModel=filterModel, db=db)


@router.get('/uploads/{image_name}')
def getImage (
    image_name: str,
):
    if image_name:
        imagePath = f"uploads/{image_name}"
        if  os.path.exists(imagePath):
            return FileResponse(imagePath)
        else:
            return "no"



# , response_model=ProductModel
@router.post('/product/create', name="admn_product_create", status_code=201)
def create(
    # accessUser: Annotated[AuthUser, Depends(auth_service2.getAccessUser)],
    category: str = Form(...),
    name: str = Form(...),
    description: str = Form(...),
    price: int = Form(...),
    id: int = Form(...),
    unit: int = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    os.makedirs('uploads', exist_ok=True)
    
    if image:
        image_path = f"uploads/{image.filename}"
        with open(image_path, "wb") as image_file:
            image_file.write(image.file.read())
        
    productCategory_repo = ProductCategoryRepository(db)
    product_repo = ProductRepository(db)
    
    productCategory = productCategory_repo.findOneName(name = category)
    if not productCategory:
        return http.notFoundResponse(message="ProductCategory not found")

    product = product_repo.findOneName(id = productCategory.id, name = name)
    if product:
        raise HTTPException(status_code=400, detail="Product already exists")
    
    model = {
        "name": name,
        "description": description,
        "price": price,
        "unit": unit,
        "categoryId": productCategory.id,
        "userCreatedId": id,
        "category": productCategory,
        "imagePath": image_path if image else None,
        "startDate": datetime.datetime.utcnow(),
        "endDate": datetime.datetime.utcnow()
    }

    productCreated = Product(**model)

    db.add(productCreated)
    db.commit()
    db.refresh(productCreated)

    result = jsonable_encoder(productCreated)

    return JSONResponse(result)


@router.put('/product/{id}/update', response_model=ProductModel, name="admn_product_update")
def update(
    id: Annotated[int, Path(title="Product id")],
    name: str = Form(...),
    description: str = Form(...),
    price: int = Form(...),
    authUserId: int = Form(...),
    unit: int = Form(...),
    image: UploadFile = File(...),
    # accessUser: Annotated[AuthUser, Depends(auth_service2.getAccessUser)],
    db: Session = Depends(get_db)
):
    product_repo = ProductRepository(db)
    
    product = product_repo.findOneId(id)
    if not product:
        return http.notFoundResponse("Product not found")
    
    product.name = name
    if description:
        product.description = description
    product.price = price
    product.unit = unit
    product.userCreatedId = authUserId
    
    if image and image.filename:
        os.makedirs('uploads', exist_ok=True)
        image_path = f"uploads/{image.filename}"
        with open(image_path, "wb") as image_file:
            image_file.write(image.file.read())
        product.imagePath = image_path

    db.commit()
    db.refresh(product)    
    
    result = jsonable_encoder(product)

    return JSONResponse(result)


def indexDetailAll(
    categoryId: int = Path(..., title="productCategory ID"),
    accessUser: AuthUser = Depends(auth_service2.getAccessUser),
    filterModel: ProductPaginateResponseModel = None,
    db: Session = Depends(get_db)
):
    product_repo = ProductRepository(db)
    products = product_repo.findOneCategoryIdFilter(model=filterModel, categoryId=categoryId)
    if not products:
        raise HTTPException(status_code=404, detail="Product not found")

    return http.successResponse(data=products)


@router.get('/{categoryId}/product', response_model=List[ProductModel], name="admn_product_category_detail_index")
def getDetailIndex (
    categoryId: int = Path(..., title="productCategory ID"),
    accessUser: AuthUser = Depends(auth_service2.getAccessUser),
    filterModel: ProductPaginateResponseModel = None,
    db: Session = Depends(get_db)
):
    return indexDetailAll(accessUser=accessUser, filterModel=filterModel, categoryId=categoryId, db=db)


@router.post('/{categoryId}/product', response_model=List[ProductModel], name="admn_product_category_detail_index")
def postDetailIndex (
    db: Session = Depends(get_db),
    categoryId: int = Path(..., title="productCategory ID"),    
    accessUser: AuthUser = Depends(auth_service2.getAccessUser),
    filterModel: ProductPaginateResponseModel = None,
):
    return indexDetailAll(accessUser=accessUser, filterModel=filterModel, categoryId=categoryId, db=db)


@router.get('/{categoryId}/unit', name="admn_product_category_unit")
def unit (
    accessUser: Annotated[AuthUser, Depends(auth_service2.getAccessUser)],
    categoryId: Annotated[int, Path(title="productCategory ID")],
    db: Session = Depends(get_db)
):
    product_repo = ProductRepository(db)
    
    product = product_repo.findOneCategoryId(categoryId)
    if not product:
        return http.notFoundResponse(message="Product not found")
    
    unit = {"unit": 0,
            "productUnit": 0}
    
    for item in product:
        if item and item.name:
            unit["productUnit"] += 1

    for item in product:
        if item and item.unit:
            unit["unit"] += int(item.unit)

    return http.successResponse(data = unit)


@router.get('/product/{id}/detail', response_model=ProductModel, name="admn_product_detail")
def detail (
    accessUser: Annotated[AuthUser, Depends(auth_service2.getAccessUser)],
    id: Annotated[int, Path(title="Product ID")],
    db: Session = Depends(get_db)
):
    repo = ProductRepository(db)
    product = repo.findOneId(id)

    if not product:
        return http.notFoundResponse(message="Product not found")

    return http.successResponse(data = product)


# @router.delete('/product/{id}/delete', response_model=ProductModel, name="admn_product_delete")
# def delete(
#     id: Annotated[int, Path(title="Product id")],
#     accessUser: Annotated[AuthUser, Depends(auth_service2.getAccessUser)],
#     db: Session = Depends(get_db)
# ):
#     repo = ProductRepository(db)
#     productDb = repo.find(id)
#     if not productDb:
#         return http.notFoundResponse("Product not found")

#     productDb.isDeleted = True
#     db.commit()
#     db.refresh(productDb)

#     productModel = ProductModel(**productDb.__dict__)
#     return http.successResponse(data=productModel, message="Product deleted")