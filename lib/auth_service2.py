from datetime import datetime, timedelta
from typing import Annotated
from fastapi import Depends, Request, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from jose.constants import ALGORITHMS
from passlib.context import CryptContext
from sqlalchemy.orm import Session, joinedload
from config import env
from config.database import get_db

# Schema
from schema.auth_module import AuthUser
# Model
from model.modules.auth import models


SECRET_KEY = "" if env.SECRET_KEY == None else env.SECRET_KEY
ALGORITHM = ALGORITHMS.HS256

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="_api/token")
pwdContext = CryptContext(schemes=["bcrypt"], deprecated="auto")


def passwordVerify(plain_password, hashed_password):
    return pwdContext.verify(plain_password, hashed_password)


def passwordHash(password):
    return pwdContext.hash(password)


def createTokenJWT(data: dict, expires_delta: timedelta):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    issuedAt = datetime.utcnow()

    to_encode.update({"exp": expire, "iat": issuedAt})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def getAccessUser(
    request: Request,
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # route: APIRoute = request.scope.get("route")
        # if route != None: 
        #     print("Route found: " + route.name)
        # else:
        #     print("Route not found raise exception")

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        tokenPayload = models.TokenPayloadModel(**payload)
        userInfo = tokenPayload.user
        
        if userInfo is None:
            raise credentials_exception
        
    except JWTError:
        raise credentials_exception
    

    authUser = db.query(AuthUser)\
            .filter(AuthUser.id == userInfo.id).first()


    if authUser is None:
        raise credentials_exception
    return authUser