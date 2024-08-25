from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_date
from users.models import Payment
from lms.models import Course, Lesson
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Populate Payment table with initial data'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        user = User.objects.first()
        course = Course.objects.first()
        lesson = Lesson.objects.first()

        Payment.objects.create(
            user=user,
            payment_date=parse_date('2024-08-25'),
            paid_course=course,
            paid_lesson=None,
            payment_amount=100.00,
            payment_method='cash'
        )
        Payment.objects.create(
            user=user,
            payment_date=parse_date('2024-08-26'),
            paid_course=None,
            paid_lesson=lesson,
            payment_amount=50.00,
            payment_method='transfer'
        )
        self.stdout.write(self.style.SUCCESS('Successfully populated Payment table'))
