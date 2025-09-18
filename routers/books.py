from fastapi import APIRouter

from fastapi import Depends, HTTPException, status, Path
from typing import Annotated
from sqlalchemy.orm import Session
import models
from models import Books
from database import SessionLocal
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
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


class BookRequest(BaseModel):
    title: str = Field(..., description="Title of the book")
    author: str = Field(..., description="Author of the book")
    published_year: Optional[int] = Field(None, ge=0, le=2100, description="Year the book was published")
    available_copies: int = Field(1, ge=0, description="Number of copies available")


@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    return db.query(Books).all()


@router.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_book(db: db_dependency, book_id: int = Path(gt=0)):
    book_model = db.query(Books).filter(Books.id == book_id).first()
    if book_model is not None:
        return book_model
    raise HTTPException(status_code=404, detail="Book not found")



@router.post("/books", status_code=status.HTTP_201_CREATED)
async def add_book(db: db_dependency, book_request: BookRequest):
    book_model = Books(**book_request.dict())
    db.add(book_model)
    db.commit()    


@router.put("/book/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(db: db_dependency, book_id: int, book_request: BookRequest):
    book_model = db.query(Books).filter(Books.id == book_id).first()
    if book_model is None:
        raise HTTPException(status_code=404, detail="Book not found")

    book_model.title = book_request.title
    book_model.author = book_request.author
    book_model.published_year = book_request.published_year
    book_model.available_copies = book_request.available_copies
    db.add(book_model)
    db.commit()



@router.delete("/book/{book_id}")
async def delete_book(db: db_dependency, book_id: int = Path(gt=0)):
    book_model = db.query(Books).filter(Books.id == book_id).first()
    if book_model is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    db.query(Books).filter(Books.id == book_id).delete()
    db.commit()
