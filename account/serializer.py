from rest_framework import serializers
from datetime import datetime
from django.conf import settings

from django.utils.timezone import now
from .models import (
    Account,
    Company,
  
)



class AccountSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = [
            "accountId",
            "first_name",
            "last_name",
            "role",
            "companyId",
            "mobile",
            "email",
            "is_active",
            "username",
            "verified",
            "photo_url"        ]
    # def get_photo_url(self, obj):
    #     if not obj.photo:
    #         return None
        
    #     request = self.context.get('request')
        
    #     # Ensure it doesn't duplicate /media/
    #     photo_url = obj.photo.url
    #     if request:
    #         return request.build_absolute_uri(photo_url)
    #     return photo_url
    def get_photo_url(self, obj):
        request = self.context.get("request")
        if obj.photo:  # assuming your model field is `photo = models.ImageField(...)`
            url = obj.photo.url
            if request:
                return request.build_absolute_uri(url)
            return url
        return None

class CompanySerializer(serializers.ModelSerializer):
    owner_id = serializers.CharField(source="owner.id")
    owner_first_name = serializers.CharField(source="owner.first_name")
    owner_last_name = serializers.CharField(source="owner.last_name")
    owner_email = serializers.CharField(source="owner.email")

    class Meta:
        model = Company
        fields = [
            "id",
            "name",
            "owner_id",
            "owner_first_name",
            "owner_last_name",
            "owner_email",
        ]