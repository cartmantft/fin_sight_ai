



from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.dialects.postgresql import UUID
import uuid
from pydantic import BaseModel

DATABASE_URL = "postgresql://postgres:1234@localhost/postgres"  # 데이터베이스 URL

engine = create_engine(DATABASE_URL)
Base = declarative_base()

class Item(Base):
    __tablename__ = "items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, index=True)
    description = Column(String)

Base.metadata.create_all(bind=engine)

def get_db():
    db = sessionmaker(autocommit=False, autoflush=False, bind=engine)()
    try:
        yield db
    finally:
        db.close()

class ItemCreate(BaseModel):
    name: str
    description: str

app = FastAPI()

origins = [
    "http://localhost:3000",  # 프런트엔드 개발 서버 주소
    # 필요에 따라 다른 origin 추가
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    print("Request received at /")  # 추가된 print 문
    return {"message": "Hello, FinSight AI Backend!"}

@app.post("/items/")
async def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = Item(name=item.name, description=item.description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
