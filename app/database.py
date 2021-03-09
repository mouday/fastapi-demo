# -*- coding: utf-8 -*-
"""
一些参考资料

sqlalchemy的基本操作大全
https://www.taodudu.cc/news/show-175725.html

Python3+SQLAlchemy+Sqlite3实现ORM教程
https://www.cnblogs.com/jiangxiaobo/p/12350561.html

SQLAlchemy 基础知识 - autoflush 和 autocommit
https://zhuanlan.zhihu.com/p/48994990

"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = 'sqlite:///data.sqlite'

# doc: https://docs.sqlalchemy.org/en/13/core/engines.html#sqlalchemy.create_engine
engine = create_engine(
    DATABASE_URL,
    encoding='utf-8',
    echo=True,  # 打印sql
    connect_args={
        'check_same_thread': False  # sqlite数据库，让任意线程可以使用
    }
)

# crud通过session会话进行
Session = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,  # 提交事务
    expire_on_commit=True,
)

# 基类
Base = declarative_base(bind=engine, name="Base")


async def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
