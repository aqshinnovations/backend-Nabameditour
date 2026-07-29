from rest_framework import serializers
from .models import Category,Doctor


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name_en", "name_ar"]



class DoctorsSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    # created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    # updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Doctor
        fields = [
                "id",
                "category",
                "name_en",
                "name_ar",
                "about_en",
                "about_ar",
                "experience_en",
                "experience_ar",
                "qualification_en",
                "qualification_ar",
                "specialist_en",
                "specialist_ar",
                "image",
                # "created_at",
                # "updated_at",
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

    def get_category(self, obj):
        if obj.category:
            return CategoriesSerializer(obj.category).data
        return None



