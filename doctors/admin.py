from django.contrib import admin
from .models import Category, Doctor, Qualification, Specialist


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name_en", "name_ar", "created_at")
    search_fields = ("name_en", "name_ar")
    ordering = ("-created_at",)


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name_en",
        "category",
        "experience_en",
        "get_specialists",
        "get_qualifications",
    )

    search_fields = ("name_en", "name_ar")
    list_filter = ("category",)

    def get_specialists(self, obj):
        return ", ".join(
            obj.specialists.values_list("name_en", flat=True)
        )

    get_specialists.short_description = "Specialists"

    def get_qualifications(self, obj):
        return ", ".join(
            obj.qualifications.values_list("name_en", flat=True)
        )

    get_qualifications.short_description = "Qualifications"


@admin.register(Qualification)
class QualificationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "doctor",
        "name_en",
        "name_ar",
    )
    search_fields = ("name_en", "doctor__name_en")


@admin.register(Specialist)
class SpecialistAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "doctor",
        "name_en",
        "name_ar",
    )
    search_fields = ("name_en", "doctor__name_en")