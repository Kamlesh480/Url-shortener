from django.db import models
from django.utils import timezone
from datetime import timedelta

class ShortenedURL(models.Model):
    long_url = models.URLField()
    short_code = models.CharField(max_length=8, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_expired(self):
        return timezone.now() > self.expires_at