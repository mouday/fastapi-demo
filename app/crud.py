# -*- coding: utf-8 -*-
from sqlalchemy.orm import Session

from .models import City, Data
from .schemas import CreateCity, CreateData


def get_city(db: Session, city_id: int):
    return db.query(City).filter(City.id == city_id).first()


def get_city_by_name(db: Session, city_name: str):
    return db.query(City).filter(City.province == city_name).first()


def get_cities(db: Session, skip: int = 0, limit: int = 10):
    return db.query(City).offset(skip).limit(limit).all()


def create_city(db: Session, city: CreateCity):
    db_city = City(**city.dict())
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def get_data(db: Session, city: str = None, skip: int = 0, limit: int = 10):
    if city:
        return db.query(Data).filter(Data.city.has(province=city))

    else:
        return db.query(Data).offset(skip).limit(limit).all()


def create_city_data(db: Session, data: CreateData, city_id: int):
    db_data = Data(**data.dict(), city_id=city_id)
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data
