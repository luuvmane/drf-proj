from django.core.exceptions import ValidationError
from urllib.parse import urlparse


class YouTubeURLValidator:
    """
    Валидатор для проверки, что URL указывает на видео с youtube.com.
    """
    def __init__(self, field=None):
        self.field = field

    def __call__(self, value):
        parsed_url = urlparse(value)
        if parsed_url.netloc != 'www.youtube.com' and parsed_url.netloc != 'youtube.com':
            raise ValidationError('URL должен быть на youtube.com.')