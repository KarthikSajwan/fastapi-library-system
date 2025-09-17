from database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime
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
    joined_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))

