from django.db import models

from django.db import models


class Testimonial(models.Model):
    image = models.ImageField(
        upload_to="testimonials/",
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return f"Testimonial {self.id}"