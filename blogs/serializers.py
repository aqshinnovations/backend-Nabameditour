from rest_framework import serializers
from datetime import datetime
from django.conf import settings

from django.utils.timezone import now
from .models import (
    Blogs
  
)

class BlogsSerializer(serializers.ModelSerializer):
    cover_image = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    class Meta:
        model = Blogs
        fields = [
            "id",
            "title",
            "content",
            "author",
            "cover_image",
            "created_at",    
            "updated_at",
       
        ]

    def get_cover_image(self, obj):
        if obj.cover_image and hasattr(obj.cover_image, "url"):
            return obj.cover_image.url  
        return None

