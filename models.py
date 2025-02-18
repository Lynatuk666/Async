from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import Integer, String

POSTGRES_DB = "super_people"
POSTGRES_PASSWORD = "password"
POSTGRES_USER = "postgres"
POSTGRES_HOST = "localhost"
POSTGRES_PORT = "5432"

PG_DSN = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_async_engine(PG_DSN)
Session = async_sessionmaker(bind=engine, expire_on_commit=False)

class Base(DeclarativeBase, AsyncAttrs):
    pass

class Person(Base):
    __tablename__ = "super_person"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    birth_year: Mapped[str] = mapped_column(String(100))
    eye_color: Mapped[str] = mapped_column(String(100))
    films: Mapped[str] = mapped_column(String(1000))
    gender: Mapped[str] = mapped_column(String(100))
    hair_color: Mapped[str] = mapped_column(String(100))
    height: Mapped[str] = mapped_column(String(100))
    homeworld: Mapped[str] = mapped_column(String(100))
    mass: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(100))
    skin_color: Mapped[str] = mapped_column(String(100))
    species: Mapped[str] = mapped_column(String(100))
    starships: Mapped[str] = mapped_column(String(1000))
    vehicles: Mapped[str] = mapped_column(String(100))

async def int_orm():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def close_orm():
    await engine.dispose()


