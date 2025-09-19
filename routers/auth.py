from fastapi import APIRouter, Depends
from pydantic import BaseModel, EmailStr
from models import Members
from passlib.context import CryptContext
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session

router = APIRouter()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class CreateMemberRequest(BaseModel):
    name: str
    email: EmailStr
    password: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/auth/")
async def create_user(create_member_request: CreateMemberRequest):
    create_member_model = Members(
        name=create_member_request.name,
        email=create_member_request.email,
        hashed_password=bcrypt_context.hash(create_member_request.password),
        role="member"
    )
    return create_member_model