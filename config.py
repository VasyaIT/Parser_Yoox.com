from enum import Enum
from os import environ

from dotenv import load_dotenv

load_dotenv()

# DataBase
DB_HOST = environ.get('POSTGRES_HOST')
DB_PORT = environ.get('POSTGRES_PORT')
DB_NAME = environ.get('POSTGRES_NAME')
DB_USER = environ.get('POSTGRES_USER')
DB_PASSWORD = environ.get('POSTGRES_PASSWORD')

# Redis
REDIS_HOST = environ.get('REDIS_HOST')
REDIS_PORT = environ.get('REDIS_PORT')

BRANDS = (1035, 9619)


class GenderTypes(str, Enum):
    men = 'men'
    women = 'women'
    boys = 'boys'
    girls = 'girls'
