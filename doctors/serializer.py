from rest_framework import serializers
from .models import Category,Doctor,Qualification,Specialist,Awards,Images


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name_en", "name_ar"]



class DoctorsSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

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
               "position_ar",
               "position_en",
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

    def get_category(self, obj):
        if obj.category:
            return CategoriesSerializer(obj.category).data
        return None



class QualificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qualification
        fields = ["id", "name_en", "name_ar"]


class SpecialistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialist
        fields = ["id", "name_en", "name_ar"]
        
class AwardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Awards
        fields = ["id", "name_en", "name_ar"]

class ImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Images
        fields = ["id", "image"]

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image:
            return (
                request.build_absolute_uri(obj.image.url)
                if request
                else obj.image.url
            )
        return None
class DoctorsDetailSerializer(DoctorsSerializer):
    category = CategoriesSerializer(read_only=True)
    qualifications = QualificationSerializer(many=True, read_only=True)
    awards = AwardSerializer(many=True, read_only=True)
    specialists = SpecialistSerializer(many=True, read_only=True)
    images = ImageSerializer(many=True, read_only=True)   # <-- Add this

    image = serializers.SerializerMethodField()

    class Meta:
        model = Doctor
        fields = [
            "id",
            "category",
            "name_en",
            "name_ar",
            "about_en",
            "about_ar",
            "position_ar",
            "position_en",
            "experience_en",
            "experience_ar",
            "qualifications",
            "specialists",
            "awards",
            "image",
            "images",     

        ]
        
    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None