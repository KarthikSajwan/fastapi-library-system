from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from models import Members
from passlib.context import CryptContext
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

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

@router.post("/auth/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency,
                      create_member_request: CreateMemberRequest):
    create_member_model = Members(
        name=create_member_request.name,
        email=create_member_request.email,
        hashed_password=bcrypt_context.hash(create_member_request.password),
        role="member"
    )
    db.add(create_member_model)
    db.commit()

@router.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    return "token"