# -*- coding: utf-8 -*-


from fastapi import APIRouter, status, Form, File, UploadFile, HTTPException
from pydantic import BaseModel

app04 = APIRouter()

"""
1、响应模型
"""


class UserInfo(BaseModel):
    name: str
    age: int


@app04.get('/response', response_model=UserInfo)
def get_response():
    """获取响应"""
    return {'name': 'Tom', 'age': '23', 'school': 'PKing'}


"""
2、响应状态码
"""


@app04.get('/status', status_code=status.HTTP_201_CREATED)
def get_status():
    """获取响应"""
    return {'status': 20}


"""
3、表单处理
"""


@app04.post('/form')
def post_form(
        username: str = Form(...),
        password: str = Form(...)):
    """Form 类需要 pip install python-multipart"""
    return {'username': username, 'password': password}


"""
4、单文件、多文件上传
"""


@app04.post('/file')
def post_file(file: bytes = File(...)):
    # 多个文件：files: List[bytes] = File(...)
    """以字节形式写入内存，适合小文件上传"""
    return {'file_size': len(file)}


@app04.post('/upload_file')
def upload_file(file: UploadFile = File(...)):
    """
        <p>UploadFile的优势:
        <p>1、文件存储到内存，内存达到阈值后保存到磁盘</p>
        <p>2、适合图片、视频大文件</p>
        <p>3、可以获取上传文件的元数据，如：文件名、创建时间等</p>
        <p>4、有文件对象的异步接口</p>
        <p>5、上传的文件是Python文件对象，可以使用：read/write/close/seek</p>
    """
    return {'filename': file.filename, 'content_type': file.content_type}


"""
5、静态文件
见 run.py
"""

"""
6、路径配置
"""


@app04.post('/config',
            response_model=UserInfo,
            summary='this is summary',
            description='this is description',
            response_description='this is response_description',
            deprecated=True,
            status_code=status.HTTP_200_OK,
            tags=['2020-01-01', '2020-01-02', '2020-01-03']
            )
def config():
    return {'key': 'value'}


"""
7、FastAPI常见配置
见 run.py
"""

"""
8、错误处理
"""


@app04.post('/exception')
def exception():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='错误信息')
