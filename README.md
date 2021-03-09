# 高性能 FastAPI 框架入门精讲

完整代码：[https://github.com/liaogx/fastapi-tutorial](https://github.com/liaogx/fastapi-tutorial)

## FastAPI的基础依赖

FastAPI文档：[https://fastapi.tiangolo.com/zh/](https://fastapi.tiangolo.com/zh/)

1. Python 3.6+

2. Python类型提示 type hints

3. Starlette 是一种轻量级的ASGI框架/工具包，是构建高性能Asyncio服务的理想选择

4. [Pydantic](https://pydantic-docs.helpmanual.io/) 是一个基于Python类型提示来定义数据验证，序列化和文档（使用JSON模式）库

## ASGI 服务器

1. ASGI异步 [Uvicorn](http://www.uvicorn.org/)、Hypercorn、Daphne

2. WSGI同步 uWSGI、Gunicorn

## 环境搭建

使用[pyenv](https://github.com/pyenv/pyenv) 创建Python虚拟环境

```bash
# 1、安装pyenv 
# 参考 https://github.com/pyenv/pyenv-installer
$ curl https://pyenv.run | bash

# 检查
$ pyenv -v

# 2、创建虚拟环境 
# 参考 https://github.com/pyenv/pyenv-virtualenv
$ pyenv virtualenv 3.7.0 fast-api-370

# 3、设置项目版本，会生成.python-version；同时，需要设置PyCharm的Python版本
# 参考 https://github.com/pyenv/pyenv
$ pyenv local fast-api-370

```

## 接口实现示例

```python
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

```

## 接口文档

http://127.0.0.1:8000/docs

http://127.0.0.1:8000/redoc

## 请求参数

函数的顺序就是路由的顺序

```python
# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Optional, List

from fastapi import APIRouter, Path, Query, Cookie, Header
from enum import Enum

from pydantic import BaseModel, Field

app03 = APIRouter()

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

```

依赖注入

在编程中，为了保证代码成功运行，先导入或声明所需要的依赖，如：子函数，数据库连接等
提高代码复用率
共享数据库连接
增强安全，认证，和角色管理

FastAPI的兼容性
所有关系型数据库，支撑NoSQL数据库
第三方的包和API
认证和授权系统
响应数据注入系统


OAuth2.0的授权模式

授权码授权模式 Authorization Code Grant
隐式授权模式 Implicit Grant
密码授权模式 Resource Owner Password Credentials Grant
客户端凭证授权模式 Client Credentials Grant


前端UI
semantic-ui: https://semantic-ui.com/


```bash
# 锁定依赖
$ pip freeze > requirements.txt 
```

工程目录结构规范

中间件：

```
Request -> 中间件 -> App -> 中间件 -> Response
```

COVID-19开源数据：
https://coronavirus-tracker-api.herokuapp.com/
