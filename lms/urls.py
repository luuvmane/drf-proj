from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, LessonListCreateView, LessonRetrieveUpdateDestroyView
from .views import SubscriptionCreateView, SubscriptionDeleteView


router = DefaultRouter()
router.register(r'courses', CourseViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('lessons/', LessonListCreateView.as_view(), name='lesson-list-create'),
    path('lessons/<int:pk>/', LessonRetrieveUpdateDestroyView.as_view(), name='lesson-retrieve-update-destroy'),
    path('subscriptions/', SubscriptionCreateView.as_view(), name='subscription-create'),
    path('subscriptions/<int:course_id>/', SubscriptionDeleteView.as_view(), name='subscription-delete'),
]
