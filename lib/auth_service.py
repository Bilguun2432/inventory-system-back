from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from config.database import get_db
from sqlalchemy.orm import Session, joinedload
import os

# Schema
from schema.auth_module import AuthUser
# Model
from model.modules.auth import models


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="_api/token")
pwdContext = CryptContext(schemes=["bcrypt"], deprecated="auto")


def passwordVerify(plain_password, hashed_password):
    return pwdContext.verify(plain_password, hashed_password)


def passwordHash(password):
    return pwdContext.hash(password)


def createAccessToken(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    # jwt.decode
    print("asdasdasds")
    return encoded_jwt


async def getTokenUser(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = models.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    

    authUser = db.query(AuthUser)\
            .options(joinedload(AuthUser.roles))\
            .filter(AuthUser.email == username).first()


    if authUser is None:
        raise credentials_exception
    return authUser