from django.utils import timezone
from .models import ShortenedURL
from .utils import generate_crc32_hash
from datetime import timedelta

class URLShortenerService:
    EXPIRY_DAYS = 30

    @staticmethod
    def create_short_url(long_url):
        code = generate_crc32_hash(long_url)

        # Check if already exists and not expired
        existing = ShortenedURL.objects.filter(short_code=code).first()
        if existing:
            if existing.is_expired():
                existing.delete()
            else:
                return existing

        expires_at = timezone.now() + timedelta(days=URLShortenerService.EXPIRY_DAYS)
        new_url = ShortenedURL.objects.create(
            long_url=long_url,
            short_code=code,
            expires_at=expires_at
        )
        return new_url

    @staticmethod
    def get_long_url(short_code):
        entry = ShortenedURL.objects.filter(short_code=short_code).first()
        if entry and not entry.is_expired():
            return entry.long_url
        return None
