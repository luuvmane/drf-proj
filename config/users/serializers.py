from rest_framework import serializers
from .models import Payment


class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'payment_date', 'payment_amount', 'payment_method', 'paid_course', 'paid_lesson', 'user']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)
