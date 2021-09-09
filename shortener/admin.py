from django.contrib import admin
from .models import Shortener


@admin.register(Shortener)
class ShortenerAdmin(admin.ModelAdmin):
    list_display = ("long_url", "short_url", "created", "times_followed")
