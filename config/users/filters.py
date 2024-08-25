import django_filters
from .models import Payments


class PaymentFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(field_name='payment_date', lookup_expr='exact')
    date_after = django_filters.DateFilter(field_name='payment_date', lookup_expr='gte')
    date_before = django_filters.DateFilter(field_name='payment_date', lookup_expr='lte')
    course = django_filters.NumberFilter(field_name='course', lookup_expr='exact')
    lesson = django_filters.NumberFilter(field_name='lesson', lookup_expr='exact')
    payment_method = django_filters.ChoiceFilter(field_name='payment_method', choices=Payments.PAYMENT_METHOD_CHOICES)
    ordering = django_filters.OrderingFilter(
        fields=(
            ('payment_date', 'date'),
        )
    )

    class Meta:
        model = Payments
        fields = ['payment_date', 'course', 'lesson', 'payment_method']
