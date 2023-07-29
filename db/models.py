from typing import Sequence

from sqlalchemy import String, Integer, ARRAY, Enum, Column
from sqlalchemy.orm import declarative_base, mapped_column, Mapped

from config import GenderTypes

Base = declarative_base()


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    brand: Mapped[str] = mapped_column(String, nullable=False)
    category: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    colors: Mapped[Sequence] = mapped_column(ARRAY(String), nullable=False)
    sizes: Mapped[Sequence] = mapped_column(ARRAY(String), nullable=False)
    images: Mapped[Sequence] = mapped_column(ARRAY(String), nullable=False)
    gender: GenderTypes = Column(Enum(GenderTypes), nullable=False)
