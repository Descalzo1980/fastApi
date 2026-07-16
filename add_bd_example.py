import uvicorn
from sqlalchemy import Integer
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from fastapi import FastAPI

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

if __name__ == "__main__":
    uvicorn.run("add_bd_example:app", reload=True)
