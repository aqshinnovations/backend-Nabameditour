from django.contrib import admin
from .models import Category, Doctor


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name_en", "name_ar", "created_at")
    search_fields = ("name_en", "name_ar")
    ordering = ("-created_at",)


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = (
        "name_en",
        "about_en",
        "category",
        "experience_en",
        "specialist_en"
    )
    search_fields = (
        "name_en",
        "name_ar",
        "specialist_en",
        "specialist_ar",
    )
    list_filter = ("category",)