# shortener/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect, get_object_or_404

from .models import ShortenedURL
from .services import URLShortenerService

class ShortenURLView(APIView):
    def post(self, request):
        original_url = request.data.get("url")
        if not original_url:
            return Response({"error": "URL is required"}, status=status.HTTP_400_BAD_REQUEST)

        short_url_obj = URLShortenerService.create_short_url(original_url)
        return Response({
            "short_url": f"http://localhost:8000/{short_url_obj.short_code}",
            "expires_at": short_url_obj.expires_at
        })

class RedirectURLView(APIView):
    def get(self, request, code):
        obj = get_object_or_404(ShortenedURL, short_code=code)

        if obj.is_expired():
            return Response({"error": "Link has expired."}, status=status.HTTP_410_GONE)

        return redirect(obj.long_url)