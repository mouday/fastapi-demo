# -*- coding: utf-8 -*-
import time

from fastapi import FastAPI, Depends, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from fastapi.middleware import Middleware
from fastapi.responses import PlainTextResponse
from fastapi.exceptions import HTTPException, RequestValidationError

import uvicorn

from tutorial import app03, app04, app05, app06, app07
from app.main import app07 as app071

from tutorial.chapter05 import verify_token

# 全局依赖
from tutorial.chapter08 import app08

app = FastAPI(
    title="FastAPI 接口文档",
    description="description",
    version="0.1.2",
    docs_url='/docs'
    # dependencies=[Depends(verify_token)]
)

# 允许跨域 协议://域名:端口
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        'http://127.0.0.1',
        'http://127.0.0.1:8080'
    ],
    allow_methods='*',
    allow_headers="*",
    allow_credentials=True
)

# 自定义http中间件
# 带yield的依赖，退出部分代码和 后台任务 会在中间件之后运行
@app.middleware('http')
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    # 自定义header以 "X-" 开头
    response.headers['X-Process-Time'] = str(process_time)
    return response


# 将子应用加到路由
app.include_router(app03, prefix='/chapter03', tags=['第三章 请求参数和验证'])
app.include_router(app04, prefix='/chapter04', tags=['第四章 响应处理和FastAPI配置'])
app.include_router(app05, prefix='/chapter05', tags=['第五章 FastAPI依赖注入系统'])
app.include_router(app06, prefix='/chapter06', tags=['第六章 安全、认证和授权'])
app.include_router(app071, prefix='/chapter07', tags=['第七章 数据库和模板'])
app.include_router(app07, prefix='/chapter07', tags=['第七章 数据库和模板'])
app.include_router(app08, prefix='/chapter08', tags=['第八章 后台任务'])

# 需要安装 pip install aiofiles
app.mount(path='/static', app=StaticFiles(directory='./static'), name='static')

# 重写异常处理器
# @app.exception_handler(HTTPException)
# def http_exception_handler(request, exception: HTTPException):
#     return PlainTextResponse(content=str(exception.detail), status_code=exception.status_code)
#
#
# @app.exception_handler(RequestValidationError)
# def validation_exception_handler(request, exception: HTTPException):
#     return PlainTextResponse(content=str(exception.detail), status_code=exception.status_code)


if __name__ == '__main__':
    # 相当于：启动服务 uvicorn run:app --reload
    uvicorn.run(app='run:app', debug=True, reload=True)
    #     http://127.0.0.1:8000
