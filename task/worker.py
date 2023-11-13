from datetime import timedelta
from task.app import app
from celery import Celery
from lib.logger.factory import getFileLogger

@app.task
def add():
    logger = getFileLogger("task")
    logger.info("Logging from task")