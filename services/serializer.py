from rest_framework import serializers
from .models import Services

class ServicesSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Services
        fields = [
                "id",
                "name_en",
                "name_ar",
                "description_en",
                "description_ar",
                "image",
                "created_at",
                "updated_at",
            ]

    def get_image(self, obj):
        request = self.context.get("request")

        if obj.image:
            return (
                request.build_absolute_uri(obj.image.url)
                if request
                else obj.image.url
            )
        return None



