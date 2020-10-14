from celery import shared_task, task
from django.core.management import call_command

from .matching import generate_notifications, generate_notifications



@shared_task(ignore_result=True)
def deactivate_old_requests():
    call_command('delete_old_requests')


@shared_task(ignore_result=True)
def delete_old_matches():
    call_command('delete_old_matches')

@shared_task(ignore_result=True)
def look_for_matches():
    return look_for_matches()

@shared_task(ignore_result=True)
def send_request_notifications():
    return generate_notifications()