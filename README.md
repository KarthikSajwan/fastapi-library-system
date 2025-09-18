# fastapi-library-system

A FastAPI-powered backend for managing a library’s books, members, and borrow/return records.  
**Note:** This project is still under development.

## Purpose
This project provides a RESTful API for a library management system, allowing you to:
- Add, update, delete, and list books.
- Manage library members.
- Record and manage book borrowings and returns.
- Authenticate users.

## Main Features & Endpoints

### Authentication
- `GET /auth/` — Check authentication status.

### Book Management
- `GET /` — List all books.
- `GET /books/{book_id}` — Get details of a book.
- `POST /books` — Add a new book.
- `PUT /book/{book_id}` — Update an existing book.
- `DELETE /book/{book_id}` — Remove a book.

### Member Management
- `GET /members_all` — List all members.
- `GET /members/{member_id}` — Get member details.
- `POST /member` — Add a new member.
- `PUT /member/{member_id}` — Update member info.
- `DELETE /member/{member_id}` — Remove a member.

### Borrow Records
- `POST /borrow` — Record borrowing of a book by a member.

## Tech Stack
- Python
- FastAPI
- SQLAlchemy
- SQLite (default database)

## Installation

```bash
git clone https://github.com/KarthikSajwan/fastapi-library-system.git
cd fastapi-library-system
pip install -r requirements.txt
```

## Usage

```bash
uvicorn main:app --reload
```

Visit [http://localhost:8000/docs](http://localhost:8000/docs) for interactive API documentation.

## Contributing

Feel free to fork and submit pull requests!  
Open to suggestions and improvements as development is ongoing.

## License

This project currently has no license.

## Status

🚧 **In Development:** Features, endpoints, and documentation are subject to change.
