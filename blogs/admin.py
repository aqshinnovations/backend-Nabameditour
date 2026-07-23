
from django.contrib import admin
from .models import Blogs


@admin.register(Blogs)
class BlogAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "author",
        "created_at",
    )

    search_fields = (
        "title",
        "author",
    )

    list_filter = (
        "created_at",
    )