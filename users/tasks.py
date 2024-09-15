from celery import shared_task
from django.utils import timezone
from django.contrib.auth.models import User


@shared_task
def check_inactive_users():
    today = timezone.now()
    month_ago = today - timezone.timedelta(days=30)
    inactive_users = User.objects.filter(last_login__lt=month_ago, is_active=True)

    for user in inactive_users:
        user.is_active = False
        user.save()
