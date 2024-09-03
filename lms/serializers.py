from rest_framework import serializers
from .models import Course, Lesson
from .validators import YouTubeURLValidator
from .models import Subscription


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['title', 'description', 'video_url']


class CourseSerializer(serializers.ModelSerializer):
    number_of_lessons = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['title', 'preview', 'description', 'number_of_lessons', 'lessons']

    def get_number_of_lessons(self, obj):
        return obj.lessons.count()


class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.URLField(validators=[YouTubeURLValidator()])

    class Meta:
        model = Lesson
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['user', 'course']