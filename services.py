from typing import Dict, Sequence

from sqlalchemy import insert
from sqlalchemy.exc import IntegrityError

from db.db import async_session_maker
from db.models import Product


async def insert_product(data: Sequence[Dict[str, str | int | Sequence[str]]]) -> None:
    async with async_session_maker() as session:
        await session.execute(insert(Product).values(data))
        try:
            await session.commit()
        except IntegrityError:
            await session.rollback()
        except Exception as e:
            print(e)
            await session.rollback()
