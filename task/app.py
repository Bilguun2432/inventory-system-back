from datetime import timedelta
from celery import Celery, shared_task
from lib.logger.factory import getFileLogger


app = Celery(
    "tasks", 
    broker="pyamqp://guest:guest@localhost:5672",
    backend="rpc://",
    serializer="json",
    )

app.conf.beat_schedule = {
    "periodic_task": {
        "task": "task.app.my_periodic_task",
        "schedule": timedelta(seconds=5)
    }
}

@app.task(bind=True)
def my_periodic_task(self):
    logger = getFileLogger("task")
    logger.info("Periodic task")


