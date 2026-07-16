import uvicorn
from pydantic import BaseModel
from sqlalchemy import Integer, select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from fastapi import FastAPI, Depends
from typing import Annotated


app = FastAPI()


engine = create_async_engine(
    "sqlite+aiosqlite:///books.db",
    echo=True
)

new_session = async_sessionmaker(
    engine,
    expire_on_commit=False
)


async def get_session():
    async with new_session() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_session)]

class Base(DeclarativeBase):
    pass


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column()
    author: Mapped[str] = mapped_column()


@app.post("/setup_database")
async def create_table():
    async with engine.begin() as conn:
        await conn.run_sync(
            lambda sync_conn: Base.metadata.create_all(sync_conn)
        )
    return {"status": "ok"}

class BookSchema(BaseModel):
    id: int
    title: str
    author: str

    class Config:
        from_attributes = True

@app.get("/books", response_model=list[BookSchema])
async def get_books(
    session = Depends(get_session)
):
    result = await session.execute(
        select(Book)
    )

    return result.scalars().all()

class BookAddSchema(BaseModel):
    id: int
    title: str
    author: str

@app.post("/books")
async def add_book(data: BookAddSchema, session:SessionDep):
    new_book = Book(
        id=data.id,
        title=data.title,
        author=data.author,
    )
    session.add(new_book)
    await session.commit()
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)