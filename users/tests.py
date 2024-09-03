from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from lms.models import Course, Lesson
from .models import Payment


class PaymentTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='testuser@example.com',
            username='testuser',  # Необходимо для создания пользователя
            password='testpassword'
        )
        self.course = Course.objects.create(
            title='Test Course',
            description='Test Description'
        )
        self.lesson = Lesson.objects.create(
            title='Test Lesson',
            description='Test Lesson Description',
            course=self.course,  # Обязательно указываем курс
            video_url='http://example.com/video'
        )
        self.valid_payload = {
            'payment_date': '2024-08-25',
            'payment_amount': 100.00,
            'payment_method': 'cash',
            'paid_course': self.course.id,
            'paid_lesson': self.lesson.id
        }
        self.invalid_payload = {
            'payment_date': '',
            'payment_amount': 'invalid',
            'payment_method': 'invalid_method',
            'paid_course': None,
            'paid_lesson': None
        }

    def test_create_payment(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/payments/', self.valid_payload, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Payment.objects.count(), 1)
        self.assertEqual(Payment.objects.get().payment_amount, 100.00)

    def test_create_payment_invalid(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/payments/', self.invalid_payload, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Payment.objects.count(), 0)
