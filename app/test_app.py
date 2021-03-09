# -*- coding: utf-8 -*-
# pytest 测试用例
from fastapi.testclient import TestClient
from run import app

# pip install pytest
client = TestClient(app)


# 执行测试 $ pytest

def test_get_data():
    response = client.post(url='/chapter07/prefix')
    assert response.status_code == 307
