import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from starlette.responses import JSONResponse

app = FastAPI()


@app.get("/", summary="Ручка", tags=["Некий главный сервис"])
def home():
    return {"message": "Hello World"}


books = [
    {
        "id": 1,
        "title": "Некая книжка",
        "author": "Пупкин",
    },
    {
        "id": 2,
        "title": "Синяя книжка",
        "author": "Пампум",
    },
]


@app.get(
    "/books",
    tags=["Книги"],
    summary="Получить все книги",
)
def read_books():
    return JSONResponse(
        content=books,
        media_type="application/json; charset=utf-8"
    )


@app.get(
    "/books/{book_id}",
    tags=["Книги"],
    summary="Получить конкретную книгу",
)
def read_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return JSONResponse(
                content=book,
                media_type="application/json; charset=utf-8"
            )
    raise HTTPException(status_code=404, detail="Нет такой книги")


class NewBook(BaseModel):
    title: str
    author: str


@app.post(
    "/books",
    tags=["Книги"],
    summary="Добавить книгу",
)
def create_book(new_book: NewBook):
    books.append(
        {
            "id": len(books) + 1,
            "title": new_book.title,
            "author": new_book.author,
        }
    )
    return { "success": True, "message": "Книга успешно добавлена" }


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
