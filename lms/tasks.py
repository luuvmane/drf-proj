from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_course_update_email(course_name, subscribers_emails):
    subject = f'Обновление курса: {course_name}'
    message = f'Курс "{course_name}" был обновлен. Проверьте новые материалы!'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, subscribers_emails)
