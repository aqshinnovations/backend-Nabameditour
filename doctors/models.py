from django.db import models


class Category(models.Model):
    name_en = models.CharField(max_length=255, blank=True, null=True)
    name_ar = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name_en or ""

    @staticmethod
    def get_by_name(name_en):
        return Category.objects.filter(name_en=name_en).first()


class Doctor(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="doctors",
    )

    name_en = models.CharField(max_length=255, blank=True, null=True)
    name_ar = models.CharField(max_length=255, blank=True, null=True)

    about_en = models.TextField(blank=True, null=True)
    about_ar = models.TextField(blank=True, null=True)

    experience_en = models.CharField(max_length=255, blank=True, null=True)
    experience_ar = models.CharField(max_length=255, blank=True, null=True)

    qualification_en = models.CharField(max_length=255, blank=True, null=True)
    qualification_ar = models.CharField(max_length=255, blank=True, null=True)

    specialist_en = models.CharField(max_length=255, blank=True, null=True)
    specialist_ar = models.CharField(max_length=255, blank=True, null=True)

    image = models.ImageField(upload_to="doctors/", blank=True, null=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.name_en or ""