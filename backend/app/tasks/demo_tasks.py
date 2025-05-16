# for demo purpose

# imports
from celery import shared_task


@shared_task
def demo():
    return "celery is detecting task perfectly!"
