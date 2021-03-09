# -*- coding: utf-8 -*-
from datetime import timedelta, datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose.constants import ALGORITHMS
from pydantic import BaseModel

app06 = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl='/chapter06/token')


@app06.get('/index')
def index(token: str = Depends(oauth2)):
    return {'token': token}


user_db = {
    'user1': {
        'username': 'user1',
        # 123456
        'hashed_password': '$2b$12$yzdcVaLu/T7KJMBP9lYDOOukdit.U1itO5PNM3aCsbvhAwPb3AXtG',
        'disabled': False
    },
    'user2': {
        'username': 'user2',
        'hashed_password': 'fakepassword2',
        'disabled': True
    }
}


def get_hash_password(password):
    return 'fake' + password


class UserInfo(BaseModel):
    username: str
    disabled: bool


class UserInfoInDB(UserInfo):
    hashed_password: str


def get_user(db, username: str):
    """"""
    if username in db:
        user_dict = db[username]
        return UserInfo(**user_dict)


def fake_decode_token(token: str):
    """"""
    user = get_user(user_db, token)
    return user


def get_current_user(token: str = Depends(oauth2)):
    """获取当前用户"""
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid Authenticate',
            headers={'WWW-Authenticate': 'Bearer'}  # auth2.0规范
        )
    return user


def get_current_active_user(current_user: UserInfo = Depends(get_current_user)):
    """获取活跃用户"""
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='未激活的用户',

        )
    return current_user


@app06.post('/token')
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = user_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='无效的用户',
        )

    user = UserInfoInDB(**user_dict)
    hashed_password = get_hash_password(form_data.password)

    if hashed_password != user.hashed_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='账号或密码不正确',
        )
    return {'access_token': user.username, 'token_type': 'bearer'}


@app06.get('/active')
def get_active_user(active_user: UserInfo = Depends(get_current_active_user)):
    return active_user


"""JWT"""

from passlib.context import CryptContext
from jose import jwt, JWTError

# 生成秘钥
# $ openssl rand -hex 32

SECRET_KEY = "1fab3266575d2b8edbb6ae9f5eeb6246abd4bbf66beaf37df43b6c6ab466d961"

ALGORITHM = ALGORITHMS.HS256  # 算法

ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 过期时间


class Token(BaseModel):
    """返回给用户的token"""
    access_token: str
    token_type: str


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

oauth2_schema = OAuth2PasswordBearer(tokenUrl='/chapter06/jwt/token')


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def jwt_get_user(username: str):
    if username in user_db:
        user_dict = user_db[username]
        return UserInfoInDB(**user_dict)


def jwt_authenticate_user(username: str, password: str):
    user = jwt_get_user(username=username)

    if not user:
        return False

    if not verify_password(plain_password=password, hashed_password=user.hashed_password):
        return False

    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()

    if not expires_delta:
        expires_delta = timedelta(minutes=15)

    expire = datetime.utcnow() + expires_delta

    to_encode.update({'exp': expire})

    encode_jwt = jwt.encode(claims=to_encode, key=SECRET_KEY, algorithm=ALGORITHM)

    return encode_jwt


@app06.post('/jwt/token', response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """"""
    user = jwt_authenticate_user(username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'}  # auth2.0规范
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        data={'sub': user.username},
        expires_delta=access_token_expires
    )

    return {'access_token': access_token, 'token_type': 'bearer'}


async def jwt_get_current_user(token: str = Depends(oauth2_schema)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid credentials',
        headers={'WWW-Authenticate': 'Bearer'}  # auth2.0规范
    )

    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get('sub')
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = jwt_get_user(username=username)
    if not user:
        raise credentials_exception

    return user


async def jwt_get_current_active_user(current_user: UserInfo = Depends(jwt_get_current_user)):
    """获取活跃用户"""
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='未激活的用户',

        )
    return current_user


@app06.get('/jwt/users/me')
def jwt_get_user_me(current_user: UserInfo = Depends(jwt_get_current_active_user)):
    return current_user
