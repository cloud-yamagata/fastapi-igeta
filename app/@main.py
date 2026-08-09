from contextlib import asynccontextmanager
from pydantic import BaseModel, ConfigDict
from pydantic_settings import BaseSettings
from pydantic.alias_generators import to_camel, to_pascal# pydanticに標準搭載された
from typing import Any, List, Optional
import datetime
from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Field, Session, SQLModel, create_engine, select
from sqlalchemy import Column, Text, SmallInteger, asc
from sqlalchemy import Boolean as SA_Boolean
from sqlalchemy.dialects.postgresql import JSONB
from .models import items
from .routers import users, items
from pydantic.alias_generators import to_camel

import pandas as pd
import json

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Initializing database...")
    #await init_db()
    yield
    print("Shutting down...")

class SQLModel(SQLModel):
    model_config = ConfigDict(
        alias_generator=to_pascal,
        populate_by_name=True,
        arbitrary_types_allowed=True,
        validate_assignment=True,
        use_enum_values=True
	)

class TeMaterial(SQLModel, table=True):
    __tablename__ = 'te_material'
    material_no : int | None = Field(default=None, primary_key=True) #原料NO
    year : int #年度
    purchase : str #仕入先
    purchase_no : str #仕入NO
    purchase_date : datetime.date #仕入日
    variety : str #品種
    tea_life : str #茶期
    organic_class : str #有機区分
    tea_type : str #茶種
    tea_rank : str #品柄
    field_no : str #圃場
    producer : str #生産者
    cost : int #原価
    material_name : str #原料名
    unit_weight : float #梱包重量
    unit_number : int #梱包数
    fraction_weight : float #端数重量
    fraction_number : int #端数本数
    remarks : str #摘要
    update_time : datetime.datetime

class TrItem(SQLModel, table=True):
    __tablename__ = 'tr_item'
    item_no : int | None = Field(default=None, primary_key=True) #商品NO
    system_class : str #システム区分
    organic_class : str #有機区分
    item_group_no : int #商品分類NO
    item_name : str #商品名
    jan_code : str #JANコード
    package_size : int #梱包サイズ
    display_order : int #表示順
    display : str #表示
    remarks : str #備考

class TeMonthlyPlan(SQLModel, table=True):
    __tablename__ = 'te_monthly_plan'
    plan_no : int | None = Field(default=None, primary_key=True) #計画NO
    year : int #年
    month : int #月
    process_type : str #工程分類
    lot_name : str #ロット名
    work_date : datetime.date #作業日
    work_time : datetime.time | None = None #作業時間
    unit_weight : int #梱包重量
    item_no : int | None = None #商品NO
    remarks : str | None = None #摘要
    # JSONB は DB により list / dict / null など型がぶれるため、検証は緩めておく（厳密にすると GET が 500 になりやすい）
    lot_part_info: Any | None = Field(default=None, sa_column=Column(JSONB))  # 使用部品情報

class TrConstant(SQLModel, table=True):
    __tablename__ = 'tr_constant'
    const_field: str | None = Field(default=None, primary_key=True)
    const: str | None = Field(default=None, primary_key=True)
    const_name: str
    display_order:int
    display : str #表示

class MonthlyPlanDeleteRow(BaseModel):
    plan_no: Optional[int] = None
    planNo: Optional[int] = None

class MonthlyPlanDeleteRequest(BaseModel):
    plans: List[MonthlyPlanDeleteRow] = []

class MonthlyPlanDeleteResponse(BaseModel):
    deleted_count: int

class MonthlyPlanUpsertPayload(BaseModel):
    planNo: Optional[int] = None
    year: int
    month: int
    processType: str
    lotName: str
    workDate: datetime.date
    workTime: datetime.time | None = None
    unitWeight: int
    itemNo: int | None = None
    remarks: str | None = None
    lotPartInfo: object | None = None

# SQLAlchemyエンジンを作成
db_url = "postgresql://igeta:igeta@localhost:5432/igeta"
engine=create_engine(db_url)

def get_session():
    with Session(engine) as session:
        yield session

#global te_material_sv = []
#def read_TeMaterial():
with Session(engine) as session:
    statement = select(TeMaterial)
    te_material = session.exec(statement)
#    global te_material = te_material
#        print(a)

#print(te_material)

#Session = (Depends(get_session))
#te_material = session.exec(select(TeMaterial))

#read_TeMaterial()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(items.router)

@app.get("/te_material/", response_model=List[TeMaterial])
def read_TeMaterial(session: Session = Depends(get_session)):
    return list(session.exec(select(TeMaterial)).all())
#def read_TeMaterial():
#     return te_material

@app.get("/tr_item/", response_model=List[TrItem])
def read_TrItem(session: Session = Depends(get_session)):
    return list(session.exec(select(TrItem)).all())

@app.get("/tr_constant/", response_model=List[TrConstant])
def read_TrConstant(session: Session = Depends(get_session)):
    return list(session.exec(select(TrConstant)).all())
#def read_tr_constant(
#    const_field: Optional[str] = Query(None),
#    session: Session = Depends(get_session)
#):
#    """システム定数。const_field を指定したときはその項目のみ。並び: const → display_order"""
#    stmt = select(TrConstant)
#    if const_field is not None and str(const_field).strip() != "":
#        stmt = stmt.where(TrConstant.const_field == str(const_field).strip())
#    stmt = stmt.order_by(asc(TrConstant.const_value), asc(TrConstant.display_order))
#    return list(session.exec(stmt).all())

@app.get("/te_monthly_plan/", response_model=List[TeMonthlyPlan])
def read_TeMonthlyPlan(session: Session = Depends(get_session)):
    return list(session.exec(select(TeMonthlyPlan)).all())

def apply_monthly_plan_payload(row: TeMonthlyPlan, payload: MonthlyPlanUpsertPayload) -> TeMonthlyPlan:
    row.year = payload.year
    row.month = payload.month
    row.process_type = payload.processType
    row.lot_name = payload.lotName
    row.work_date = payload.workDate
    row.work_time = payload.workTime
    row.unit_weight = payload.unitWeight
    row.item_no = payload.itemNo
    row.remarks = payload.remarks
    row.lot_part_info = payload.lotPartInfo if payload.lotPartInfo is not None else []
    return row

def delete_monthly_plan_records(
    *,
    session: Session,
    targets: List[MonthlyPlanDeleteRow]
) -> int:
    plan_no_list = []
    for target in targets:
        plan_no = target.plan_no if target.plan_no is not None else target.planNo
        if isinstance(plan_no, int):
            plan_no_list.append(plan_no)

    if len(plan_no_list) == 0:
        return 0

    plan_no_set = set(plan_no_list)
    statement = select(TeMonthlyPlan).where(TeMonthlyPlan.plan_no.in_(plan_no_set))
    rows = session.exec(statement).all()

    deleted_count = 0
    for row in rows:
        session.delete(row)
        deleted_count += 1

    session.commit()
    return deleted_count

@app.post("/te_monthly_plan/delete", response_model=MonthlyPlanDeleteResponse)
def delete_te_monthly_plan(
    payload: MonthlyPlanDeleteRequest,
    session: Session = Depends(get_session)
):
    deleted_count = delete_monthly_plan_records(session=session, targets=payload.plans)
    return MonthlyPlanDeleteResponse(deleted_count=deleted_count)

@app.post("/te_monthly_plan/create", response_model=TeMonthlyPlan)
def create_te_monthly_plan(
    payload: MonthlyPlanUpsertPayload,
    session: Session = Depends(get_session)
):
    row = TeMonthlyPlan(
        plan_no=payload.planNo,
        year=payload.year,
        month=payload.month,
        process_type=payload.processType,
        lot_name=payload.lotName,
        work_date=payload.workDate,
        work_time=payload.workTime,
        unit_weight=payload.unitWeight,
        item_no=payload.itemNo,
        remarks=payload.remarks,
        lot_part_info=[]
    )
    row = apply_monthly_plan_payload(row, payload)
    session.add(row)
    session.commit()
    session.refresh(row)
    return row

@app.post("/te_monthly_plan/update", response_model=TeMonthlyPlan)
def update_te_monthly_plan(
    payload: MonthlyPlanUpsertPayload,
    session: Session = Depends(get_session)
):
    if payload.planNo is None:
        raise HTTPException(status_code=400, detail="planNo is required")

    row = session.get(TeMonthlyPlan, payload.planNo)
    if row is None:
        raise HTTPException(status_code=404, detail="Monthly plan not found")

    row = apply_monthly_plan_payload(row, payload)
    session.add(row)
    session.commit()
    session.refresh(row)
    return row