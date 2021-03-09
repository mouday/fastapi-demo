# -*- coding: utf-8 -*-

from datetime import datetime, date as _date
from pydantic import BaseModel


class CreateData(BaseModel):
    date: _date
    confirmed: int = 0
    deaths: int = 0
    recovered: int = 0


class ReadData(CreateData):
    id: int
    city_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class CreateCity(BaseModel):
    province: str
    country: str
    country_code: str
    country_population: str


class ReadCity(CreateCity):
    id: int

    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
