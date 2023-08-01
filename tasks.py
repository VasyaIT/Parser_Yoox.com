from celery import Celery
from celery.schedules import crontab

from config import REDIS_HOST, REDIS_PORT
from main import main

app = Celery('yoox', broker=f'redis://{REDIS_HOST}:{REDIS_PORT}')


@app.task()
def startup(launch: int):
    main(launch)


app.conf.beat_schedule = {
    # Executes every day at 12:00 a.m.
    'add-every-day-midnight': {
        'task': 'tasks.startup',
        'schedule': crontab(minute='0', hour='0'),
        'args': (0,)
    },
    # Executes every day at 06:00 a.m.
    'add-every-day-06:00': {
        'task': 'tasks.startup',
        'schedule': crontab(minute='0', hour='6'),
        'args': (1,)
    },
    # Executes every day at 12:00 p.m.
    'add-every-day-12:00': {
        'task': 'tasks.startup',
        'schedule': crontab(minute='0', hour='12'),
        'args': (2,)
    },
    # Executes every day at 6:00 p.m.
    'add-every-day-18:00': {
        'task': 'tasks.startup',
        'schedule': crontab(minute='0', hour='18'),
        'args': (3,)
    },
}
