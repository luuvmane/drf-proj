from django.contrib import admin
from .models import CustomUser, Payment


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'phone', 'city')
    search_fields = ('email', 'username')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'payment_date', 'payment_amount', 'payment_method', 'paid_course', 'paid_lesson')
    search_fields = ('user__email', 'payment_method')
