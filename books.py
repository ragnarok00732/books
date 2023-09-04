from fastapi import FastAPI, HTTPException
from pydantic import BaseModel,field_validator

class Book(BaseModel):
    id: int
    title: str
    author: str
    year_published: int
    edition: str

    @field_validator('year_published')
    def validate_year_published(cls, year_published):
        if year_published < 0 or year_published > 2023:
            raise ValueError("Published year must be between 0 and 2023")
        return year_published

app = FastAPI()

books = [
    {
        "id": 1,
        "title": "Harry Potter and the Philosopher's Stone",
        "author": "J. K. Rowling",
        "year_published": 1997,
        "edition": "First",
    },
    {
        "id": 2,
        "title": "The Lord Of The Rings",
        "author": "J. R. R. Tolkien",
        "year_published": 1954,
        "edition": "First",
    },
    {
        "id": 3,
        "title": "The Hobbit",
        "author": "J. R. R. Tolkien",
        "year_published": 1954,
        "edition": "First",
    },
]

@app.get("/", tags=["root"])
async def root() -> dict:
    return {"Interesting Books API": "v1.0.0"}


@app.get("/books/", tags=["books"], response_model=list[Book])  
async def get_books() -> list[Book]:
    return books


@app.get("/books/{book_id}", tags=["books"], response_model=Book)
async def get_book(book_id: int) -> Book:
    for book in books:
        if book["id"] == book_id:
            return Book(**book)
    raise HTTPException(status_code=404, detail="Book not found")


@app.post("/books/", tags=["books"], response_model=Book)
async def create_book(book: Book) -> Book:
    new_id = max(book["id"] for book in books) + 1
    book_dict = book.dict()
    book_dict["id"] = new_id
    books.append(book_dict)
    return Book(**book_dict)


@app.put("/books/{book_id}", tags=["books"], response_model=Book)
async def update_book(book_id: int, updated_book: Book) -> Book:
    for i, book in enumerate(books):
        if book["id"] == book_id:
            books[i] = updated_book()
            books[i]["id"] = book_id
            return updated_book
    raise HTTPException(status_code=404, detail="Book not found")


@app.delete("/books/{book_id}", tags=["books"])
async def delete_book(book_id: int) -> dict:
    for book in books:
        if book["id"] == book_id:
            books.remove(book)
            return {"message": "Book deleted"}
