from celery import shared_task


@shared_task
def deactivate_inactive_users():
    pass
