from celery import shared_task
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


@shared_task
def check_inactive_users():
    today = timezone.now()
    month_ago = today - timezone.timedelta(days=30)

    inactive_users = User.objects.filter(last_login__lt=month_ago, is_active=True)

    if inactive_users.exists():
        inactive_users.update(is_active=False)