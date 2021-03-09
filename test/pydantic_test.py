# -*- coding: utf-8 -*-
"""

文档 https://pydantic-docs.helpmanual.io/
Github https://github.com/samuelcolvin/pydantic/

安装
```
pip install pydantic
```
"""

from datetime import datetime, date
from pathlib import Path
from typing import List, Optional

from pydantic import BaseModel, ValidationError, constr
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.declarative import declarative_base


def print_color(text):
    """PyCharm控制台打印带颜色的文字"""
    print(f"\033[31m===== {text} =====\033[0m")


print_color("1、基本使用")


class User(BaseModel):
    id: int  # 无默认值，必填字段
    name = 'John Doe'  # 有默认值，选填字段
    signup_ts: Optional[datetime] = None  # 选填字段
    friends: List[int] = []  # 列表中的元素是int类型或者是可以转换成int类型的其他类型


external_data = {
    'id': '123',
    'signup_ts': '2017-06-01 12:22',
    'friends': [1, '2', b'3']
}

user = User(**external_data)
print(user)
# > User id=123 name='John Doe' signup_ts=datetime.datetime(2017, 6, 1, 12, 22) friends=[1, 2, 3]

print(user.id)
# > 123


print_color("2、错误校验")

error_data = {
    'id': 'a123',
    'signup_ts': '2017-06-01 12:22',
    'friends': [1, '2', '3']
}

try:
    User(**error_data)
except ValidationError as e:
    print(e.json())
"""
[
  {
    "loc": [
      "id"
    ],
    "msg": "value is not a valid integer",
    "type": "type_error.integer"
  }
]
"""

print_color("3、模型类的属性和方法")

# 实例方法
print(user.dict())
print(user.json())
print(user.copy())  # 浅拷贝
print(user.schema())
print(user.schema_json())
"""
{'id': 123, 'signup_ts': datetime.datetime(2017, 6, 1, 12, 22), 'friends': [1, 2, 3], 'name': 'John Doe'}
{"id": 123, "signup_ts": "2017-06-01T12:22:00", "friends": [1, 2, 3], "name": "John Doe"}
id=123 signup_ts=datetime.datetime(2017, 6, 1, 12, 22) friends=[1, 2, 3] name='John Doe'
{
    'title': 'User', 
    'type': 'object', 
    'properties': {
        'id': {
            'title': 'Id', 
            'type': 'integer'
            }, 
        'signup_ts': {
            'title': 'Signup Ts', 
            'type': 'string', 
            'format': 'date-time'
            }, 
        'friends': {
            'title': 'Friends', 
            'default': [], 
            'type': 'array', 
            'items': {'type': 'integer'}
            }, 
        'name': {
            'title': 'Name', 
            'default': 'John Doe', 
            'type': 'string'
            }
        }, 
    'required': ['id']
}

{
    "title": "User", 
    "type": "object", 
    "properties": {
        "id": {"title": "Id", "type": "integer"}, 
        "signup_ts": {"title": "Signup Ts", "type": "string", "format": "date-time"}, 
        "friends": {"title": "Friends", "default": [], "type": "array", "items": {"type": "integer"}}, 
        "name": {"title": "Name", "default": "John Doe", "type": "string"}}, 
    "required": ["id"]
}
"""
# 类方法
print(User.parse_obj(external_data))
print(User.parse_raw('{"id": 123, "signup_ts": "2017-06-01T12:22:00", "friends": [1, 2, 3], "name": "John Doe"}'))

path = Path("obj.json")
path.write_text('{"id": 123, "signup_ts": "2017-06-01T12:22:00", "friends": [1, 2, 3], "name": "John Doe"}')

print(User.parse_file(path))
"""
id=123 signup_ts=datetime.datetime(2017, 6, 1, 12, 22) friends=[1, 2, 3] name='John Doe'
id=123 signup_ts=datetime.datetime(2017, 6, 1, 12, 22) friends=[1, 2, 3] name='John Doe'
id=123 signup_ts=datetime.datetime(2017, 6, 1, 12, 22) friends=[1, 2, 3] name='John Doe'
"""

# 不进行数据校验
print(User.construct(path))
"""
signup_ts=None friends=[] name='John Doe'
"""

# 字段
print(User.__fields__.keys())
"""
dict_keys(['id', 'signup_ts', 'friends', 'name'])
"""

print_color("4、递归模型")


class Sound(BaseModel):
    sound: str


class Dog(BaseModel):
    name: str
    birthday: date = None
    sound: List[Sound]


dog = Dog(name="Tom", birthday=date.today(), sound=[{'sound': 'wangwang'}, {'sound': 'miaomiao'}])
print(dog.dict())
"""
{
    'name': 'Tom', 
    'birthday': datetime.date(2021, 2, 14), 
    'sound': [{'sound': 'wangwang'}, {'sound': 'miaomiao'}]
}
"""

print_color("5、ORM模型")

Base = declarative_base()


class CompanyOrm(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True, nullable=True)
    public_key = Column(String(20), index=True, nullable=True, unique=True)
    name = Column(String(63), unique=True)
    domains = Column(ARRAY(String(255)))


class CompanyMode(BaseModel):
    id: int
    public_key: constr(max_length=20)
    name: constr(max_length=63)
    domains: List[constr(max_length=255)]

    class Config:
        orm_mode = True


company_orm = CompanyOrm(
    id=123,
    public_key='foo_key',
    name='Testing',
    domains=['baidu.com', 'sina.com']
)

print(CompanyMode.from_orm(company_orm))
"""
id=123 public_key='foo_key' name='Testing' domains=['baidu.com', 'sina.com']
"""