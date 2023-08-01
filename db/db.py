from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import DB_USER, DB_HOST, DB_PASSWORD, DB_NAME

from db.models import Base


DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'

engine = create_engine(DATABASE_URL)
Session = sessionmaker(autocommit=False, bind=engine)


def recreate_tables():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
