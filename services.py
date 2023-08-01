from typing import Dict, Sequence

from sqlalchemy import insert
from sqlalchemy.exc import IntegrityError

from db.db import Session
from db.models import Product


def insert_product(data: Sequence[Dict[str, str | int | Sequence[str]]]) -> None:
    session = Session()
    session.execute(insert(Product).values(data))
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
    except Exception as e:
        print(e)
        session.rollback()
