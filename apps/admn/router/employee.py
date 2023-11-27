from typing import Annotated, List
from fastapi import Depends, HTTPException, APIRouter, Path, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from config.database import get_db

# Lib
from lib import auth_service2, http
# Model
from model.modules.employee.product_models import EmployeeProductPaginateResponseModel, AuthUserProductModel, AuthUserTransferProductModel
# Repo
from repository.employee.product_repository import EmployeeProductRepository
from repository.action.repository import ActionRepository
from repository.product.repository import AuthUserProductRepository
# Schema
from schema.auth_module import AuthUser
from schema.action_module import Action
from schema.product_module import AuthUserProduct


router = APIRouter(
    prefix="/employee",
    tags=["Employee"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found auth"}},
)


def indexProductAll(
    accessUser: Annotated[AuthUser, Depends(auth_service2.getAccessUser)],
    id: int = Path(..., title="AuthUser ID"),
    filterModel: EmployeeProductPaginateResponseModel = None,
    db: Session = Depends(get_db)
):
    employeeProduct_repo = EmployeeProductRepository(db)
    employeeProducts = employeeProduct_repo.findProducts(model=filterModel, id=id)
    if not employeeProducts:
        raise HTTPException(status_code=404, detail="AuthUser not found")
    
    return http.successResponse(data = employeeProducts)


@router.get('/{id}/product', response_model=List[AuthUserProductModel],  name="admn_auth_user_product_index")
def getProductAll(
    accessUser: Annotated[AuthUser, Depends(auth_service2.getAccessUser)],
    id: int = Path(..., title="AuthUser ID"),
    filterModel: EmployeeProductPaginateResponseModel = None,
    db: Session = Depends(get_db)
):
    return indexProductAll(accessUser=accessUser, filterModel=filterModel, id=id, db=db)

# , response_model=List[AuthUserProductModel]
@router.post("/{id}/product", name = "admn_auth_user_product_index")
def postProductIndex(
    accessUser: Annotated[AuthUser, Depends(auth_service2.getAccessUser)],
    filterModel: EmployeeProductPaginateResponseModel,
    id: int = Path(..., title="AuthUser ID"),
    db: Session = Depends(get_db)
):
    return indexProductAll(accessUser=accessUser, filterModel=filterModel, id=id, db=db)


@router.post("/transfer", name="admn_auth_user_product_transfer")
def postTransferProduct(
    accessUser: Annotated[AuthUser, Depends(auth_service2.getAccessUser)],
    transferModel: AuthUserTransferProductModel,
    db: Session = Depends(get_db)
):
    action_repo = ActionRepository(db)
    authUserProduct_repo = AuthUserProductRepository(db)
    
    authUserProduct = authUserProduct_repo.findAuthUserProduct(transferModel.authUserProduct.productId, transferModel.authUserId)
    
    authUserProduct.unit -= transferModel.transferUnit
    
    createModel = {
        "actionStatusId": transferModel.actionStatusId,
        "authUserId": transferModel.authUserId,
        "unit": transferModel.transferUnit,
        "productId": transferModel.authUserProduct.productId,
        "description": transferModel.description
    }
    
    createModel = Action(**createModel)
    
    db.add(createModel)
    db.commit()
    db.refresh(createModel)
    db.refresh(authUserProduct)
    
    jsonResult = jsonable_encoder(createModel)
    return JSONResponse(jsonResult)