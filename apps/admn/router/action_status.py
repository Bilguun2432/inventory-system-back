from typing import Annotated, List
from fastapi import Depends, HTTPException, APIRouter, Path, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from config.database import get_db

# Lib
from lib import auth_service2, http
# Model
from model.modules.action.status_models import ActionStatusModel
# Repo
from repository.action.status_repository import ActionStatusRepository
# Schema
from schema.auth_module import AuthUser


router = APIRouter(
    prefix="/action/status",
    tags=["AuthUser"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found auth"}},
)


@router.get('/', response_model=ActionStatusModel,  name="admn_action_status_all")
def getAll(
    accessUser: Annotated[AuthUser, Depends(auth_service2.getAccessUser)],
    db: Session = Depends(get_db)
):
    actionStatus_repo = ActionStatusRepository(db)
    
    actionStatuss = actionStatus_repo.findAll()
    if not actionStatuss:
        raise HTTPException(status_code=404, detail="Status not found")
    
    return http.successResponse(data=actionStatuss)