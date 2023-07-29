# This is a parser of a huge online store 'Yoox'
## Before start, create a .env file and enter the data below into it
```
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_NAME=yoox
POSTGRES_USER=postgres
POSTGRES_PASSWORD=123456

REDIS_HOST=redis
REDIS_PORT=6379
```
## In the config file.py in the BRAND constant, you can add the brand IDs you need to collect data
```BRANDS = (1035, 9619)```
## The brand ID is located in the address bar of the request:
```https://www.yoox.com/women/shoponline/#/d=1035``` - d=1035
# Start
```commandline
docker-compose up --build
```