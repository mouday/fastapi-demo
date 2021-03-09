# -*- coding: utf-8 -*-
from pprint import pprint

from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request, Response, Depends, HTTPException, status, Query, Body, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Optional, List
from pydantic import HttpUrl
from .schemas import CreateCity, CreateData, ReadCity, ReadData
from .database import Base, engine, get_db
import requests

from . import crud

app07 = APIRouter()

templates = Jinja2Templates(directory='app/templates')

Base.metadata.create_all(bind=engine)


@app07.get('/')
def index(request: Request,
          city: str = None,
          skip: int = 0,
          limit: int = 10,
          db: Session = Depends(get_db)):
    print('index')

    data = crud.get_data(db=db, city=city, skip=skip, limit=limit)

    print(data)

    return templates.TemplateResponse('home.html', {
        'request': request,
        'data': data,
        'sync_data_url': 'url'
    })


@app07.post('/createCity', response_model=ReadCity)
def create_city(city: CreateCity, db: Session = Depends(get_db)):
    db_city = crud.get_city_by_name(db=db, city_name=city.province)
    if db_city:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='city is exists')

    return crud.create_city(db=db, city=city)


@app07.get('/getCity/{city}', response_model=ReadCity)
def get_city(city: str, db: Session = Depends(get_db)):
    db_city = crud.get_city_by_name(db=db, city_name=city)
    if db_city is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='city not found')
    else:
        return db_city


@app07.post('/getCites', response_model=List[ReadCity])
def get_cites(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_cities(db=db, skip=skip, limit=limit)


@app07.post('/createData', response_model=ReadData)
def create_data(data: CreateData, city: str, db: Session = Depends(get_db)):
    db_city = crud.get_city_by_name(db=db, city_name=city)
    return crud.create_city_data(db=db, data=data, city_id=db_city.id)


@app07.get('/get_data')
def get_data(city: str = None, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    data = crud.get_data(db=db, city=city, skip=skip, limit=limit)
    return data


# 不要再后台任务导入依赖
def sync_data_task(db: Session):
    pass


@app07.get('/sync')
def sync_data(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    background_tasks.add_task(sync_data_task, db=db)

    return {
        'message': '后台处理中，稍后刷新查看'
    }
