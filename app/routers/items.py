from fastapi import APIRouter
import sqlalchemy
from sqlalchemy import create_engine, MetaData, inspect,table
from sqlalchemy.orm import sessionmaker
import psycopg2
import json

router = APIRouter()

@router.get("/items/", tags=["items"])
async def read_items(te_lot):
    for row in result:
        print(row)
    resultTe_lot = session.query(te_lot).all()
    #resultTe_lot = session.query(te_lot).all()
    #return [{"itemname": "Rick"}, {"itemname": "Morty"}]
    return json.dumps(resultTe_lot)

@router.get("/items/me", tags=["items"])
async def read_item_me():
    return {"itemname": "fakecurrentuser"}

@router.get("/items/{itemname}", tags=["items"])
async def read_item(itemname: str):
    #te_lot = sqlalchemy.Table(itemname, META_DATA, autoload_with=engine)
    #resultTe_lot = session.query(te_lot).all()
    for row in resultTe_lot:
        print(row)
    return {"itemname": itemname}