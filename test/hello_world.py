# -*- coding: utf-8 -*-
from typing import Optional
from pydantic import BaseModel

from fastapi import FastAPI

app = FastAPI()


class CityInfo(BaseModel):
    province: str
    country: str
    is_affected: Optional[bool] = None

# 同步代码
"""
@app.get("/")
def index():
    return {'hello': 'world'}


# 路径参数和查询参数
@app.get("/city/{city}")
def get_result(city: str, age: Optional[int] = None):
    return {'city': city, 'age': age}


@app.post("/city/{city}")
def post_result(city: str, cityinfo: CityInfo):
    return {'city': city, 'cityinfo': cityinfo}
"""

# 异步代码
@app.get("/")
async def index():
    return {'hello': 'world'}


# 路径参数和查询参数
@app.get("/city/{city}")
async def get_result(city: str, age: Optional[int] = None):
    return {'city': city, 'age': age}


@app.post("/city/{city}")
async def post_result(city: str, cityinfo: CityInfo):
    return {'city': city, 'cityinfo': cityinfo}

# 启动服务 uvicorn hello_world:app --reload
