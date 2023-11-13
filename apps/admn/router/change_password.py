import re
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from config.database import get_db

# Lib
from lib import auth_service2
# Model
from model.modules.auth.user_models import NewPasswordPasswordModel
# Schema
from schema.auth_module import AuthUser


router = APIRouter(
    prefix="/auth/user",
    tags=["ChangePassword"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found auth"}},
)


@router.put("/changepassword")
def change_password(
    model: NewPasswordPasswordModel,
    accessUser: Annotated[AuthUser, Depends(auth_service2.getAccessUser)],
    db: Session = Depends(get_db)
):
    
    passChange =  auth_service2.passwordVerify(model.currentpassword, accessUser.password)

    if not passChange:
        raise HTTPException(status_code=404, detail="wrong password")
    
    if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@#$%^&+=!]).{8,}$', model.password):
        raise HTTPException(status_code=400, detail="password must be Upper and lower case letters, numbers and special characters and  must be 8 characters")
    
    accessUser.password = model.password

    passwordPlain = accessUser.password
    passwordHash = auth_service2.passwordHash(passwordPlain)
    accessUser.password = passwordHash

    db.commit()
    db.refresh(accessUser)

    return jsonable_encoder(accessUser)