#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import distutils
import os
from datetime import datetime, timedelta
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from passlib.context import CryptContext
from pydantic import BaseModel
from starlette.status import HTTP_401_UNAUTHORIZED
from env.environment import Environment
from ossmodels.users import Users
from util import log

'''logging'''
env = Environment()
log = log.Logger(level=os.getenv('OSSGPAPI_APP_LOG_LEVEL'))

'''oauth2 and jwt'''

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str = None


class User(BaseModel):
    name: str
    role: str = None
    active: str = None


prefix = os.getenv('OSSGPAPI_APP_PREFIX')
if prefix.startswith('/'):
    pass
else:
    prefix = '/' + prefix

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=prefix+"/token")


def verify_password(plain_password, hashed_password):
    log.logger.debug('verify_password with hashed_password: [%s]' % hashed_password)
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    guser = db.getUsersbyname(username)
    if guser is not None:
        ruser = User(name = guser['name'],role = guser['role'],active = guser['active'])
        return ruser


def authenticate_user(fake_db, username: str, password: str):
    log.logger.debug('authenticate_user with username: [%s]' % username)
    result = fake_db.userlogin(username,password)
    if result['Authentication'] == True:
        user = get_user(fake_db, username)
        return user
    else:
        return False


def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.getenv("OSSGPAPI_APP_AUTH_SECURITY_KEY"), os.getenv("OSSGPAPI_APP_AUTH_SECURITY_ALGORITHM"))
    log.logger.debug('create_access_token with encoded_jwt: [%s]' % encoded_jwt)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, os.getenv("OSSGPAPI_APP_AUTH_SECURITY_KEY"), os.getenv("OSSGPAPI_APP_AUTH_SECURITY_ALGORITHM"))
        username: str = payload.get("name")

        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except PyJWTError:
        raise credentials_exception
    apiusers = Users()
    user = get_user(apiusers, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not distutils.util.strtobool(current_user.active):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_write_permission(current_user: User = Depends(get_current_user)):
    if not distutils.util.strtobool(current_user.active):
        raise HTTPException(status_code=400, detail="Inactive user")
    else:
        rolelist = current_user.role.strip().replace('[','').replace(']','').split(',')
        if ('admin' in set(rolelist)) or ('writer' in set(rolelist)):
            return True
        else:
            raise HTTPException(status_code=400, detail="Permission denied")


async def get_super_permission(current_user: User = Depends(get_current_user)):
    if not distutils.util.strtobool(current_user.active):
        raise HTTPException(status_code=400, detail="Inactive user")
    else:
        rolelist = current_user.role.strip().replace('[', '').replace(']', '').split(',')
        if 'admin' in set(rolelist):
            return True
        else:
            raise HTTPException(status_code=400, detail="Permission denied")

if __name__ == '__main__':
    pass
