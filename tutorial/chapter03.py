# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Optional, List

from fastapi import APIRouter, Path, Query, Cookie, Header
from enum import Enum

from pydantic import BaseModel, Field

app03 = APIRouter()

"""
函数的顺序就是路由的顺序
"""

"""
1、路径参数和数字验证
"""


# 不带路径参数
@app03.get("/path/message")
def get_message():
    return {'message': 'hello'}


# 带路径参数
@app03.get("/path/{message}")
def get_message(message: str):
    return {'message': message}


# 枚举值
class CityEnum(str, Enum):
    beijing = "Beijing"
    shanghai = "Shanghai"


@app03.get("/enum/{city}")
def get_enum(city: CityEnum):
    return {'message': city}


# 文件名参数
@app03.get("/file/{file_path:path}")
def get_file(file_path: str):
    return {'file_path': file_path}


# 数字参数
@app03.get("/num/{num}")
def get_num(num: int = Path(..., title='数字', description='不可描述', ge=1, le=10)):
    return {'num': num}


"""
2、查询参数和字符串验证
"""


# 数字转换
@app03.get("/query")
def get_page(page: int, size: Optional[int] = 20):
    return {'page': page, 'size': size}


# 布尔类型转换
@app03.get("/conversion")
def conversion(flag: bool = False):
    return {'flag': flag}


# 多个查询参数和参数别名
@app03.get("/query_params")
def query_params(
        value: str = Query(..., min_length=1, max_length=8, alias='name'),
        values: List[str] = Query(default=['v1', 'v2'], alias='names')
):
    return {'value': value, 'values': values}


"""
3、请求体参数
"""


# 请求体
class CityInfo(BaseModel):
    # example注解，值不会被验证
    name: str = Field(..., example='Beijing')
    country: str
    country_code: str = None  # 默认值
    country_population: int = Field(default=800, title='人口数量', description='国家的人口数量', ge=800)

    # 配置额外信息
    class Config:
        schema_extra = {
            'example': {
                'name': 'Shanghai',
                'country': 'China',
                'country_code': 'CN',
                'country_population': 14000000000
            }
        }


@app03.post("/body/city")
def city_info(city: CityInfo):
    return city.dict()


"""
4、混合参数 Request body + Path parameters + Query parameters
"""


@app03.post("/body/city/{name}")
def mix_city_info(
        name: str,
        city01: CityInfo,
        city02: CityInfo,
        confirmed: int = Query(ge=0, description='确诊数', default=0),
        death: int = Query(ge=0, description='死亡数', default=0)
):
    return {
        'name': name,
        'confirmed': confirmed,
        'death': death,
        'city01': city01.dict(),
        'city02': city02.dict()
    }


class Data(BaseModel):
    city_info: List[CityInfo] = None
    date: datetime
    confirmed: int = Field(ge=0, description='确诊数', default=0)
    death: int = Field(ge=0, description='死亡数', default=0)
    recovered: int = Field(ge=0, description='痊愈数', default=0)


@app03.post("/body/nested")
def nested_city_info(data: Data):
    return data


"""
5、Cookie 和 Header参数
"""


@app03.get("/body/cookie")
def cookie(cookie_id: Optional[str] = Cookie(default=None)):
    return {'cookie_id': cookie_id}


@app03.get("/body/header")
def header(cookie_id: Optional[str] = Header(default=None, convert_underscores=True)):
    """
    有些HTTP代理和服务器不允许请求头带有下划线
    :param cookie_id: header中传递示例：cookie-id: xxx
    :return:
    """
    return {'cookie_id': cookie_id}
