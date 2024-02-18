import os
from sqlalchemy.ext.asyncio import create_async_engine

from models import User, StatusChoises


# engine = create_async_engine('sqlite+aiosqlite:///example.db', echo=True)
engine = create_async_engine(
        f"postgresql+asyncpg://{os.getenv("DB_USER")}:{os.getenv("DB_PASS")}@{os.getenv("DB_HOST")}/{os.getenv("DB_NAME")}",
        echo=True,
    )

async def add_user(username, telegram_id):
    async with engine.connect() as conn:
        async with conn.begin():
            await conn.execute(User.__table__.insert().values(
                telegram_username=username, telegram_id=telegram_id
            ))

async def get_users():
    async with engine.connect() as conn:
        result = await conn.execute(User.__table__.select().where(User.status != StatusChoises.finished.value))
        users = result.fetchall()
        return users
    
async def update_user(user_id, **kwargs):
    async with engine.connect() as conn:
        async with conn.begin():
            await conn.execute(User.__table__.update().where(User.id == user_id).values(
                **kwargs
            ))
