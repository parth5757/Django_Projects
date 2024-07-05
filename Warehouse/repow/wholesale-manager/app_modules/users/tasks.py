from celery import shared_task
from services.email_service import EmailSender
import traceback

@shared_task()
def send_email_notifications(**kwargs):
    try:
        return EmailSender.send(**kwargs)
    except Exception as e:
        traceback_data = traceback.format_exc()
        print(f"==>> traceback_data: {traceback_data}")