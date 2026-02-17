from django.contrib import admin
from .models import Notice

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "created_at")
    list_filter = ("created_at", "author")
    search_fields = ("title", "body", "author__username")
    ordering = ("-created_at",)
