# -*- coding: utf-8 -*-
"""
Navicat和PyCharm自带的SQLite客户端保存Date时间格式的时候会被装换为时间戳格式，获取解析会失败

SQLite本身没有时间格式，保存使用的是NUMERIC类型
"""

from sqlalchemy import Column, Integer, BigInteger, String, DateTime, Date, ForeignKey, func
from sqlalchemy.orm import relationship
from .database import Base


class City(Base):
    __tablename__ = 'city'  # 数据表名

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    province = Column(String(100), unique=True, nullable=False, comment='省/直辖市')
    country = Column(String(1000), nullable=False, comment='国家')
    country_code = Column(String(1000), nullable=False, comment='国家代码')
    country_population = Column(BigInteger, nullable=False, comment='国家人口')
    # 关联类名：Data， 反向访问属性名：city
    data = relationship('Data', back_populates='city')

    created_at = Column(DateTime, server_default=func.now(), comment='创建时间')
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='更新时间')

    # 默认正序，倒序排列 .desc()
    __mapper_args__ = {'order_by': country_code}

    def __repr__(self):
        return f'{self.country}_{self.province}'


class Data(Base):
    __tablename__ = 'data'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    # '表名.属性名'
    city_id = Column(Integer, ForeignKey('city.id'), comment='所属省/直辖市')
    date = Column(Date, nullable=False, comment='数据日期')
    confirmed = Column(BigInteger, default=0, nullable=False, comment='确诊数')
    deaths = Column(BigInteger, default=0, nullable=False, comment='死亡数')
    recovered = Column(BigInteger, default=0, nullable=False, comment='痊愈数')
    city = relationship('City', back_populates='data')

    created_at = Column(DateTime, server_default=func.now(), comment='创建时间')
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='更新时间')

    # 默认正序，倒序排列 .desc()
    __mapper_args__ = {'order_by': date.desc()}

    def __repr__(self):
        return f'{repr(self.date)}_{self.confirmed}'
