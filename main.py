from fastapi import FastAPI, Depends, HTTPException, status, Path
from typing import Annotated
from sqlalchemy.orm import Session
import models
from models import Books, Members, BorrowRecords
from database import engine, SessionLocal
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

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

class MemberRequest(BaseModel):
    name: str = Field(..., description="Member's full name")
    email: EmailStr = Field(..., description="Member's email address")
    joined_date: Optional[datetime] = Field(None, description="Date the member joined")

class BorrowRequest(BaseModel):
    member_id: int
    book_id: int



@app.get("/", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    return db.query(Books).all()

@app.get("/members_all", status_code=status.HTTP_200_OK)
async def read_all_members(db: db_dependency):
    return db.query(Members).all()


@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_book(db: db_dependency, book_id: int = Path(gt=0)):
    book_model = db.query(Books).filter(Books.id == book_id).first()
    if book_model is not None:
        return book_model
    raise HTTPException(status_code=404, detail="Book not found")

@app.get("/members/{member_id}", status_code=status.HTTP_200_OK)
async def read_member(db: db_dependency, member_id: int = Path(gt=0)):
    member_model = db.query(Members).filter(Members.id == member_id).first()
    if member_model is not None:
        return member_model
    raise HTTPException(status_code=404, detail="Member not found")


@app.post("/books", status_code=status.HTTP_201_CREATED)
async def add_book(db: db_dependency, book_request: BookRequest):
    book_model = Books(**book_request.dict())
    db.add(book_model)
    db.commit()    

@app.post("/member", status_code=status.HTTP_201_CREATED)
async def add_member(db: db_dependency, member_request: MemberRequest):
    member_model = Members(**member_request.dict())
    db.add(member_model)
    db.commit()


@app.put("/book/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
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

@app.put("/member/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_member(db: db_dependency, member_id: int, member_request: MemberRequest):
    member_model = db.query(Members).filter(Members.id == member_id).first()
    if member_model is None:
        raise HTTPException(status_code=404, detail="Member not found")
    
    member_model.name = member_request.name
    member_model.email = member_request.email
    member_model.joined_date = member_request.joined_date
    db.add(member_model)
    db.commit()


@app.delete("/book/{book_id}")
async def delete_book(db: db_dependency, book_id: int = Path(gt=0)):
    book_model = db.query(Books).filter(Books.id == book_id).first()
    if book_model is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    db.query(Books).filter(Books.id == book_id).delete()
    db.commit()

@app.delete("/member/{member_id}")
async def delete_member(db: db_dependency, member_id: int = Path(gt=0)):
    member_model = db.query(Members).filter(Members.id == member_id).first()
    if member_model is None:
        raise HTTPException(status_code=404, detail="Member not found")
    
    db.query(Members).filter(Members.id == member_id).delete()
    db.commit()



@app.post("/borrow", status_code=status.HTTP_201_CREATED)
async def borrow_book(db: db_dependency, borrow_request: BorrowRequest):

    book_model = db.query(Books).filter(Books.id == borrow_request.book_id).first()
    if book_model is None:
        raise HTTPException(status_code=404, detail="Book not found")

    if book_model.available_copies <= 0:
        raise HTTPException(status_code=400, detail="No copies available for this book")

    # 3. Check if member exists
    member_model = db.query(Members).filter(Members.id == borrow_request.member_id).first()
    if member_model is None:
        raise HTTPException(status_code=404, detail="Member not found")

    borrow_model = BorrowRecords(
        member_id=borrow_request.member_id,
        book_id=borrow_request.book_id
    )
    db.add(borrow_model)

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
