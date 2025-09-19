from database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

class Books(Base):
    __tablename__ = "books"  # table name in DB

    id = Column(Integer, primary_key=True, index=True)  # unique ID
    title = Column(String, nullable=False, index=True)  # book title
    author = Column(String, nullable=False, index=True)  # book author
    published_year = Column(Integer, nullable=True)  # year of publishing
    available_copies = Column(Integer, default=1)  # how many copies are left
    is_available = Column(Boolean, default=True)  # quick flag for availability



class Members(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String)
    joined_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    role = Column(String)


class BorrowRecords(Base):
    __tablename__ = "borrow_records"

    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)

    borrow_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    return_date = Column(DateTime, nullable=True)  # when returned
    is_returned = Column(Boolean, default=False)   # quick flag

    # relationships
    member = relationship("Members", backref="borrow_records")
    book = relationship("Books", backref="borrow_records")

    