from fastapi import FastAPI
import models
from database import engine
from routers import auth, books, members, borrow_records

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# Register Routers
app.include_router(auth.router)
app.include_router(books.router)
app.include_router(members.router)
app.include_router(borrow_records.router)