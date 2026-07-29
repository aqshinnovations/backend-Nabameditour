from django.db import models

class Blogs(models.Model):
    LANGUAGE_CHOICES = [
        ("en", "English"),
        ("ar", "Arabic"),
    ]

    language = models.CharField(
        max_length=2,
        choices=LANGUAGE_CHOICES,
        default="en",
    )
    
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.CharField(max_length=255)
    cover_image = models.ImageField(upload_to="blogs/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return str(self.title) + " : " + str(self.author)

