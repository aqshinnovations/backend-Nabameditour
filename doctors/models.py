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

    position_en = models.CharField(max_length=255, blank=True, null=True)
    position_ar = models.CharField(max_length=255, blank=True, null=True)

    image = models.ImageField(upload_to="doctors/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.name_en or ""
class Qualification(models.Model):
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name="qualifications"
    )

    name_en = models.CharField(max_length=255)
    name_ar = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name_en


class Specialist(models.Model):
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name="specialists"
    )

    name_en = models.CharField(max_length=255)
    name_ar = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name_en
    
class Awards(models.Model):
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name="awards"
    )

    name_en = models.CharField(max_length=255)
    name_ar = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name_en

class Images(models.Model):
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(upload_to="doctor_images/")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.doctor.name_en} - {self.id}"