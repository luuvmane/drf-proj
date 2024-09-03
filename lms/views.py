from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Course, Lesson, Subscription
from .serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer
from .permissions import IsOwnerOrModerator
from users.models import Payment
from users.serializers import PaymentsSerializer
from rest_framework import filters
from .paginators import CoursePagination, LessonPagination


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]
    pagination_class = CoursePagination

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        """
        Пользователи видят и редактируют только свои курсы,
        а модераторы могут видеть и редактировать любые курсы.
        """
        queryset = super().get_queryset()
        if self.request.user.groups.filter(name='Moderators').exists():
            return queryset
        return queryset.filter(owner=self.request.user)


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]
    pagination_class = LessonPagination

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        """
        Пользователи видят и редактируют только свои уроки,
        а модераторы могут видеть и редактировать любые уроки.
        """
        queryset = super().get_queryset()
        if self.request.user.groups.filter(name='Moderators').exists():
            return queryset
        return queryset.filter(owner=self.request.user)


class LessonListCreateView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]
    pagination_class = LessonPagination

    def get_queryset(self):
        """
        Пользователи видят и создают только свои уроки,
        а модераторы могут видеть и создавать любые уроки.
        """
        queryset = super().get_queryset()
        if self.request.user.groups.filter(name='Moderators').exists():
            return queryset
        return queryset.filter(owner=self.request.user)


class LessonRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]

    def get_queryset(self):
        """
        Пользователи видят и редактируют только свои уроки,
        а модераторы могут видеть и редактировать любые уроки.
        """
        queryset = super().get_queryset()
        if self.request.user.groups.filter(name='Moderators').exists():
            return queryset
        return queryset.filter(owner=self.request.user)


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentsSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ['paid_course', 'paid_lesson', 'payment_method']
    ordering_fields = ['payment_date']
    ordering = ['-payment_date']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        """
        Пользователи видят и редактируют только свои платежи,
        а модераторы могут видеть и редактировать любые платежи.
        """
        queryset = super().get_queryset()
        if self.request.user.groups.filter(name='Moderators').exists():
            return queryset
        return queryset.filter(owner=self.request.user)


class SubscriptionCreateView(generics.CreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SubscriptionDeleteView(generics.DestroyAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        course_id = self.kwargs.get('course_id')
        return Subscription.objects.get(user=user, course_id=course_id)
