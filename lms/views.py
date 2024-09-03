from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Course, Lesson, Payment
from .serializers import CourseSerializer, LessonSerializer, PaymentsSerializer
from .permissions import IsOwnerOrModerator


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]

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
