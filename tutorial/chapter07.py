# -*- coding: utf-8 -*-

from fastapi import APIRouter, Request, Depends


async def get_user_agent(request: Request):
    print(request.headers['User-Agent'])


app07 = APIRouter(
    prefix='/prefix',
    tags=['第七章 数据库和模板'],
    dependencies=[Depends(get_user_agent)],
    responses={200: {'description': 'good job'}}
)


@app07.get('/')
def index():
    return {'message': 'hello'}
