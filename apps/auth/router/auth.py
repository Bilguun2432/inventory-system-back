from datetime import timedelta
from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from config.database import get_db

# Lib
from lib import auth_service2, auth_service
# Model
from model.modules.auth import models
# Repo
from repository.user.user_repository import UserRepository

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 4
REFRESH_TOKEN_EXPIRE_MINUTES = 1440


router = APIRouter(
    tags=["Auth"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.post("/token", response_model=models.Token, name="api_auth_token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
):
    repo = UserRepository(db)
    authUser = repo.findOneByEmail(form_data.username)
    if not authUser:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not auth_service.passwordVerify(form_data.password, authUser.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_service.createAccessToken(
        data={"sub": authUser.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login", response_model=models.AuthUserTokensModel, name="api_auth_login")
async def login(
    authData: models.AuthRequestModel,
    db: Session = Depends(get_db)
):
    repo = UserRepository(db)
    authUser = repo.findOneByEmail(authData.username)
    if not authUser:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not auth_service2.passwordVerify(authData.password, authUser.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    roleIds = []
    for authRole in authUser.roles:
        roleIds.append(authRole.id)

    userData = models.UserPayloadModel(
        id=authUser.id,
        username=authUser.email,
        email=authUser.email,
        roles=roleIds
    )

    timeExpire = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_service2.createTokenJWT(
        data={"user": userData.dict(), "type": "access"}, 
        expires_delta=timeExpire
    )

    timeExpire = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    refresh_token = auth_service2.createTokenJWT(
        data={"user": userData.dict(), "type": "refresh"}, 
        expires_delta=timeExpire
    )

    tokens = models.AuthTokensModel(
        access=access_token,
        refresh=refresh_token
    )

    result = models.AuthUserTokensModel(
        user = userData,
        tokens = tokens
    )

    return result
    # jsonResult = jsonable_encoder(result)
    # return JSONResponse(jsonResult)