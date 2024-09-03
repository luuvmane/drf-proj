from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Course, Lesson, Subscription
from users.models import CustomUser


class LessonTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(username='user1', password='password123')
        self.moderator = CustomUser.objects.create_user(username='moderator', password='password123')
        self.moderator.groups.create(name='Moderators')
        self.course = Course.objects.create(title='Course 1', description='Course Description', owner=self.user)
        self.lesson = Lesson.objects.create(title='Lesson 1', course=self.course, owner=self.user)

    def test_create_lesson_authenticated(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'New Lesson',
            'course': self.course.id,
        }
        response = self.client.post('/lessons/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_create_lesson_unauthenticated(self):
        data = {
            'title': 'New Lesson',
            'course': self.course.id,
        }
        response = self.client.post('/lessons/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_lesson_authenticated(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'Updated Lesson',
        }
        response = self.client.put(f'/lessons/{self.lesson.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, 'Updated Lesson')

    def test_delete_lesson_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/lessons/{self.lesson.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)

    def test_list_lessons_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/lessons/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_list_lessons_unauthenticated(self):
        response = self.client.get('/lessons/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class SubscriptionTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(username='user1', password='password123')
        self.course = Course.objects.create(title='Course 1', description='Course Description', owner=self.user)

    def test_subscribe_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/subscriptions/', {'course': self.course.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_subscribe_unauthenticated(self):
        response = self.client.post('/subscriptions/', {'course': self.course.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unsubscribe_authenticated(self):
        Subscription.objects.create(user=self.user, course=self.course)
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/subscriptions/{self.course.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_unsubscribe_unauthenticated(self):
        Subscription.objects.create(user=self.user, course=self.course)
        response = self.client.delete(f'/subscriptions/{self.course.id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
