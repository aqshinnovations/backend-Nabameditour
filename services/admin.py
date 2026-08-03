from django.contrib import admin

# Register your models here.
from .models import Services


@admin.register(Services)
class ServicesAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name_en",
        "description_en",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "name_en",
        "description_en",
    )
    list_filter = (
        "created_at",
        "updated_at",
    )
  