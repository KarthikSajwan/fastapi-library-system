from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from sqlalchemy.orm import Session
import models
from models import Books, Members, BorrowRecords
from database import SessionLocal
from pydantic import BaseModel

router = APIRouter()

# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


class BorrowRequest(BaseModel):
    member_id: int
    book_id: int


@router.post("/borrow", status_code=status.HTTP_201_CREATED)
async def borrow_book(db: db_dependency, borrow_request: BorrowRequest):

    # Check if book exists
    book_model = db.query(Books).filter(Books.id == borrow_request.book_id).first()
    if book_model is None:
        raise HTTPException(status_code=404, detail="Book not found")

    if book_model.available_copies <= 0:
        raise HTTPException(status_code=400, detail="No copies available for this book")

    # Check if member exists
    member_model = db.query(Members).filter(Members.id == borrow_request.member_id).first()
    if member_model is None:
        raise HTTPException(status_code=404, detail="Member not found")

    # Create borrow record
    borrow_model = BorrowRecords(
        member_id=borrow_request.member_id,
        book_id=borrow_request.book_id
    )
    db.add(borrow_model)

    # Update book copies
    book_model.available_copies -= 1
    if book_model.available_copies == 0:
        book_model.is_available = False

    db.commit()

    return {
        "message": "Book borrowed successfully",
        "member": member_model.name,
        "book": book_model.title,
        "borrow_date": borrow_model.borrow_date
    }
