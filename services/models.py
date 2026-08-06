from django.db import models

from django.db import models


class Services(models.Model):
    name_en = models.CharField(max_length=255, blank=True, null=True)
    name_ar = models.CharField(max_length=255, blank=True, null=True)
    
    position_en = models.CharField(max_length=255, blank=True, null=True)
    position_ar = models.CharField(max_length=255, blank=True, null=True)

    description_en = models.TextField(blank=True, null=True)
    description_ar = models.TextField(blank=True, null=True)

    image = models.ImageField(upload_to="services/", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Service"
        verbose_name_plural = "Services"

    def __str__(self):
        return self.name_en