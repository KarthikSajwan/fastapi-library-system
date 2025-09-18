from fastapi import APIRouter, Depends, HTTPException, status, Path
from typing import Annotated, Optional
from sqlalchemy.orm import Session
import models
from models import Members
from database import SessionLocal
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime

router = APIRouter()

# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


class MemberRequest(BaseModel):
    name: str = Field(..., description="Member's full name")
    email: EmailStr = Field(..., description="Member's email address")
    joined_date: Optional[datetime] = Field(None, description="Date the member joined")


@router.get("/members_all", status_code=status.HTTP_200_OK)
async def read_all_members(db: db_dependency):
    return db.query(Members).all()


@router.get("/members/{member_id}", status_code=status.HTTP_200_OK)
async def read_member(db: db_dependency, member_id: int = Path(gt=0)):
    member_model = db.query(Members).filter(Members.id == member_id).first()
    if member_model is not None:
        return member_model
    raise HTTPException(status_code=404, detail="Member not found")


@router.post("/member", status_code=status.HTTP_201_CREATED)
async def add_member(db: db_dependency, member_request: MemberRequest):
    member_model = Members(**member_request.dict())
    db.add(member_model)
    db.commit()


@router.put("/member/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_member(db: db_dependency, member_id: int, member_request: MemberRequest):
    member_model = db.query(Members).filter(Members.id == member_id).first()
    if member_model is None:
        raise HTTPException(status_code=404, detail="Member not found")
    
    member_model.name = member_request.name
    member_model.email = member_request.email
    member_model.joined_date = member_request.joined_date
    db.add(member_model)
    db.commit()


@router.delete("/member/{member_id}")
async def delete_member(db: db_dependency, member_id: int = Path(gt=0)):
    member_model = db.query(Members).filter(Members.id == member_id).first()
    if member_model is None:
        raise HTTPException(status_code=404, detail="Member not found")
    
    db.query(Members).filter(Members.id == member_id).delete()
    db.commit()
