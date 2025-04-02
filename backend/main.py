from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
# sqlalchemy.dialects.postgresql.UUID는 모델 정의 시 Column 타입에만 사용합니다.
from sqlalchemy.dialects.postgresql import UUID as SQLAlchemyUUID, ARRAY
import uuid # 표준 파이썬 uuid 모듈을 사용합니다.
from pydantic import BaseModel, ConfigDict # Pydantic V2용 ConfigDict 추가
import os
from datetime import datetime
from typing import Optional, List # List 타입 힌트 추가

# 표준 uuid 모듈 임포트 (이미 위에 있음)
# from sqlalchemy.orm import Session # 이미 위에 있음
# from fastapi import Depends, HTTPException, FastAPI # 이미 위에 있음

# --- 환경 변수 및 데이터베이스 설정 ---
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:1234@localhost/postgres")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # SessionLocal로 이름 변경 권장
Base = declarative_base()

# --- SQLAlchemy 모델 정의 ---
# User, Material, Summary, Tag, MaterialTag 모델 정의는 동일하게 유지
# (Column 타입에는 SQLAlchemyUUID 사용)

class User(Base):
    __tablename__ = "users"
    id = Column(SQLAlchemyUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    folders = relationship("Folder", back_populates="owner")

class Material(Base):
    __tablename__ = "materials"
    id = Column(SQLAlchemyUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, index=True)
    url = Column(String, nullable=True)
    pdf_file = Column(String, nullable=True)
    youtube_link = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    summaries = relationship("Summary", back_populates="material")
    tags = relationship("Tag", secondary="material_tag", back_populates="materials")

class Summary(Base):
    __tablename__ = "summaries"
    id = Column(SQLAlchemyUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    material_id = Column(SQLAlchemyUUID(as_uuid=True), ForeignKey("materials.id"))
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    material = relationship("Material", back_populates="summaries")

class Folder(Base):
    __tablename__ = "folders"
    id = Column(SQLAlchemyUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_id = Column(SQLAlchemyUUID(as_uuid=True), ForeignKey("users.id"))
    name = Column(String)
    owner = relationship("User", back_populates="folders")

class Tag(Base):
    __tablename__ = "tags"
    id = Column(SQLAlchemyUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, index=True)
    materials = relationship("Material", secondary="material_tag", back_populates="tags")

class MaterialTag(Base):
    __tablename__ = "material_tag"
    material_id = Column(SQLAlchemyUUID(as_uuid=True), ForeignKey("materials.id"), primary_key=True)
    tag_id = Column(SQLAlchemyUUID(as_uuid=True), ForeignKey("tags.id"), primary_key=True)

# Schedule 모델 정의 추가
class Schedule(Base):
    __tablename__ = "schedules"
    id = Column(SQLAlchemyUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_id = Column(SQLAlchemyUUID(as_uuid=True), ForeignKey("users.id"))
    name = Column(String)
    cron_expression = Column(String)
    target_url = Column(String)
    folder_id = Column(SQLAlchemyUUID(as_uuid=True), ForeignKey("folders.id"))


Base.metadata.create_all(bind=engine)

# --- 데이터베이스 세션 의존성 ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Pydantic 모델 (Schemas) 정의 ---
# Pydantic 모델에서는 표준 uuid.UUID를 사용하고, orm_mode 또는 from_attributes=True 를 사용합니다.
# arbitrary_types_allowed는 제거해도 됩니다.

class FolderBase(BaseModel):
    name: str

class FolderCreate(FolderBase):
    # owner_id는 경로 파라미터나 인증된 사용자 정보로 받는 것이 일반적입니다.
    # 여기서는 일단 요청 본문에 포함하는 것으로 가정합니다.
    owner_id: uuid.UUID # 표준 UUID 사용

class FolderUpdate(FolderBase):
    pass # name만 업데이트

class FolderResponse(FolderBase):
    id: uuid.UUID # 표준 UUID 사용
    owner_id: uuid.UUID # 표준 UUID 사용

    # Pydantic V2+
    model_config = ConfigDict(from_attributes=True)
    # Pydantic V1
    # class Config:
    #     orm_mode = True

class MaterialBase(BaseModel):
    title: str
    url: Optional[str] = None
    pdf_file: Optional[str] = None
    youtube_link: Optional[str] = None

class MaterialCreate(MaterialBase):
    pass

class MaterialResponse(MaterialBase):
    id: uuid.UUID # 표준 UUID 사용
    created_at: datetime

    # Pydantic V2+
    model_config = ConfigDict(from_attributes=True)
    # Pydantic V1
    # class Config:
    #     orm_mode = True

class SummaryBase(BaseModel):
    content: str

class SummaryCreate(SummaryBase):
    material_id: uuid.UUID # 표준 UUID 사용

class SummaryResponse(SummaryBase):
    id: uuid.UUID # 표준 UUID 사용
    material_id: uuid.UUID # 표준 UUID 사용
    created_at: datetime

    # Pydantic V2+
    model_config = ConfigDict(from_attributes=True)
    # Pydantic V1
    # class Config:
    #     orm_mode = True


class ScheduleBase(BaseModel):
    name: str
    cron_expression: str
    target_url: str
    folder_id: uuid.UUID # 표준 UUID 사용

class ScheduleCreate(ScheduleBase):
    owner_id: uuid.UUID # 표준 UUID 사용

class ScheduleUpdate(ScheduleBase):
    # owner_id는 일반적으로 업데이트하지 않음
    pass

class ScheduleResponse(ScheduleBase):
    id: uuid.UUID # 표준 UUID 사용
    owner_id: uuid.UUID # 표준 UUID 사용

    # Pydantic V2+
    model_config = ConfigDict(from_attributes=True)
    # Pydantic V1
    # class Config:
    #     orm_mode = True


# ItemCreate는 예시였으므로 제거하거나 Item 모델과 함께 완성해야 함

# --- FastAPI 앱 설정 ---
app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- API 라우트 정의 ---

@app.get("/")
async def read_root():
    print("Request received at /")
    return {"message": "Hello, FinSight AI Backend!"}

# Item 관련 라우트는 Item 모델이 정의되지 않았으므로 주석 처리 또는 삭제
# @app.post("/items/")
# async def create_item(item: ItemCreate, db: Session = Depends(get_db)):
#     # db_item = Item(...) # Item 모델 필요
#     # ...

@app.post("/materials/", response_model=MaterialResponse) # 응답 모델 지정
async def create_material(material: MaterialCreate, db: Session = Depends(get_db)):
    db_material = Material(**material.model_dump()) # Pydantic 모델 데이터 사용
    db.add(db_material)
    db.commit()
    db.refresh(db_material)
    return db_material # SQLAlchemy 객체 반환 (orm_mode/from_attributes=True 필요)

@app.post("/summaries/", response_model=SummaryResponse) # 응답 모델 지정
async def create_summary(summary: SummaryCreate, db: Session = Depends(get_db)):
    # material 존재 여부 확인 로직 추가 권장
    db_summary = Summary(**summary.model_dump())
    db.add(db_summary)
    db.commit()
    db.refresh(db_summary)
    return db_summary

@app.get("/materials/", response_model=List[MaterialResponse]) # 응답 모델 지정 (리스트)
async def search_materials(keyword: str, db: Session = Depends(get_db)):
    materials = db.query(Material).filter(Material.title.contains(keyword)).all()
    return materials

# 최근 자료 목록 조회 API 추가
@app.get("/materials/recent", response_model=List[MaterialResponse])
async def list_recent_materials(limit: int = 10, db: Session = Depends(get_db)):
    """
    최근 생성된 자료 목록을 반환합니다.
    """
    materials = db.query(Material).order_by(Material.created_at.desc()).limit(limit).all()
    return materials

@app.get("/folders/", response_model=List[FolderResponse]) # 응답 모델 지정 (리스트)
async def list_folders(db: Session = Depends(get_db)):
    folders = db.query(Folder).all()
    return folders

@app.post("/folders/", response_model=FolderResponse) # 응답 모델 지정
async def create_folder(folder: FolderCreate, db: Session = Depends(get_db)):
    # owner_id 존재 여부 확인 로직 추가 권장
    db_folder = Folder(**folder.model_dump())
    db.add(db_folder)
    db.commit()
    db.refresh(db_folder)
    return db_folder

# *** 여기가 수정된 부분 ***
# 파라미터 타입 힌트를 uuid.UUID로 변경
# 응답 모델도 FolderResponse로 명시적으로 지정
@app.put("/folders/{folderId}", response_model=FolderResponse)
async def update_folder(folderId: uuid.UUID, folder: FolderUpdate, db: Session = Depends(get_db)):
    db_folder = db.query(Folder).filter(Folder.id == folderId).first()
    if db_folder is None:
        raise HTTPException(status_code=404, detail="Folder not found")

    update_data = folder.model_dump(exclude_unset=True) # Pydantic V2
    for key, value in update_data.items():
         setattr(db_folder, key, value)

    db.commit()
    db.refresh(db_folder)
    return db_folder # SQLAlchemy 객체 반환

# *** 여기가 수정된 부분 ***
# 파라미터 타입 힌트를 uuid.UUID로 변경
@app.delete("/folders/{folderId}", status_code=200) # 성공 시 상태 코드 명시 권장
async def delete_folder(folderId: uuid.UUID, db: Session = Depends(get_db)):
    db_folder = db.query(Folder).filter(Folder.id == folderId).first()
    if db_folder is None:
        raise HTTPException(status_code=404, detail="Folder not found")
    db.delete(db_folder)
    db.commit()
    return {"message": "Folder deleted successfully"}

# --- Schedule 라우트 ---

@app.get("/schedules/", response_model=List[ScheduleResponse]) # 응답 모델 지정
async def list_schedules(db: Session = Depends(get_db)):
    schedules = db.query(Schedule).all()
    return schedules

@app.post("/schedules/", response_model=ScheduleResponse) # 응답 모델 지정
async def create_schedule(schedule: ScheduleCreate, db: Session = Depends(get_db)):
    # owner_id, folder_id 존재 여부 확인 로직 추가 권장
    db_schedule = Schedule(**schedule.model_dump())
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule

# *** 여기가 수정된 부분 ***
# 파라미터 타입 힌트를 uuid.UUID로 변경
# 응답 모델도 ScheduleResponse로 명시적으로 지정
@app.put("/schedules/{scheduleId}", response_model=ScheduleResponse)
async def update_schedule(scheduleId: uuid.UUID, schedule: ScheduleUpdate, db: Session = Depends(get_db)):
    db_schedule = db.query(Schedule).filter(Schedule.id == scheduleId).first()
    if db_schedule is None:
        raise HTTPException(status_code=404, detail="Schedule not found")

    update_data = schedule.model_dump(exclude_unset=True) # Pydantic V2
    for key, value in update_data.items():
         setattr(db_schedule, key, value)

    db.commit()
    db.refresh(db_schedule)
    return db_schedule # SQLAlchemy 객체 반환

# *** 여기가 수정된 부분 ***
# 파라미터 타입 힌트를 uuid.UUID로 변경
@app.delete("/schedules/{scheduleId}", status_code=200) # 성공 시 상태 코드 명시 권장
async def delete_schedule(scheduleId: uuid.UUID, db: Session = Depends(get_db)):
    db_schedule = db.query(Schedule).filter(Schedule.id == scheduleId).first()
    if db_schedule is None:
        raise HTTPException(status_code=404, detail="Schedule not found")
    db.delete(db_schedule)
    db.commit()
    return {"message": "Schedule deleted successfully"}

# --- 서버 실행 (개발용) ---
# 터미널에서 uvicorn main:app --reload 로 실행
