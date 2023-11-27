from datetime import datetime
from typing import Annotated, List
from fastapi import Depends, HTTPException, APIRouter, Path, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from config.database import get_db
from googletrans import Translator
from sqlalchemy import inspect

# Lib
from lib import auth_service2, http
# Model
from model.modules.transfer.transfer_models import TransferModel
from model.modules.product.auth_user_product_models import AuthUserProductModel
# Repo
from repository.transfer.transfer_repository import TransferRepository
from repository.user.user_repository import UserRepository
from repository.product.repository import ProductRepository, AuthUserProductRepository
# Schema
from schema.auth_module import AuthUser
from schema.action_module import Action, ActionStatus
from schema.product_module import AuthUserProduct


router = APIRouter(
    prefix="/transfer",
    tags=["Product"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

@router.post('/create', name="admn_transfer", status_code=201)
def create(
    transferModel: TransferModel,
    accessUser: Annotated[AuthUser, Depends(auth_service2.getAccessUser)],
    db: Session = Depends(get_db)
):
    transfer_repo = TransferRepository(db)
    authUser_repo = UserRepository(db)
    product_repo = ProductRepository(db)
    authUserProduct_repo = AuthUserProductRepository(db)
    
    authUser = authUser_repo.findOneByEmail(transferModel.email)
    if not authUser:
        raise HTTPException(status_code=404, detail="AuthUser not found")
    
    product = product_repo.findOneId(transferModel.productId)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    authUserProduct = authUserProduct_repo.findAuthUserProduct(productId = product.id, authUserId = authUser.id)
    if not authUserProduct:
        createAuthUserProductModel = {
            "userId": authUser.id,
            "productId": product.id,
            "unit": transferModel.transferUnit
        }
        
        authUserProduct = AuthUserProduct(**createAuthUserProductModel)
        
        db.add(authUserProduct)
    else:
        authUserProduct.unit += transferModel.transferUnit

    product.unit -= transferModel.transferUnit

    db.commit()

    db.refresh(product)
    db.refresh(authUserProduct)
    
    jsonResult = jsonable_encoder(authUserProduct)
    
    return JSONResponse(jsonResult)