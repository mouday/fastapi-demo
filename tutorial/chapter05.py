# -*- coding: utf-8 -*-
from typing import Optional

from fastapi import APIRouter, Depends, Header, HTTPException
from starlette import status

app05 = APIRouter()

"""
1、要依赖的函数，提高代码复用性
"""


def pagination(page: int = 1, limit: int = 20):
    return {'page': page, 'limit': limit}


@app05.get('/list_func')
def get_list_depend_func(paginate: dict = Depends(pagination)):
    return paginate


"""
2、要依赖的类
"""


class Pagination(object):
    def __init__(self, page: int = 1, limit: int = 20):
        self.page = page
        self.limit = limit


@app05.get('/list_class')  # 3中形式等价
def get_list_depend_class(paginate: Pagination = Depends()):
    # paginate: Pagination = Depends(Pagination)
    # paginate = Depends()

    return paginate


"""
3、子依赖
"""


def query(query_string: Optional[str] = None):
    print('query')
    return query_string


def sub_query(query_string: str = Depends(query)):
    print('sub_query')
    return query_string


@app05.get('/query')
def final_query(query_string: str = Depends(sub_query, use_cache=True)):
    """use_cache 多个依赖有同一个依赖时，同一个request请求只会调用子依赖一次"""
    return query_string


"""
4、路径操作装饰器中的多依赖
"""


def verify_token(x_token: str = Header(...)):
    print('verify_token')
    if not x_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='detail')


@app05.get('/verify_query', dependencies=[Depends(verify_token)])
def path_query():
    return {'success': True}


"""
5、全局依赖
见 run.py
"""

"""
6、带yield依赖
Python3.7 + 
Python3.6 pip install async-exit-stack async-generator 
"""


async def get_db():
    db = 'db_connection'
    try:
        yield db
    finally:
        print('db_close')


async def get_depend_a():
    db = 'db_connection'
    try:
        yield db
    finally:
        print('depend_a')


async def get_depend_b(depend_a=Depends(get_depend_a)):
    db = 'db_connection'
    try:
        yield db
    finally:
        print('depend_b')


async def get_depend_c(depend_b=Depends(get_depend_b)):
    db = 'db_connection'
    try:
        yield db
    finally:
        print('depend_c')
