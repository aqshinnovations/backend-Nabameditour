from rest_framework import serializers
from datetime import datetime
from django.conf import settings

from django.utils.timezone import now
from .models import (
    Hospital,Specialization
  
)

def get_translated(obj, field, lang):
    return getattr(obj, f"{field}_{lang}", None) or getattr(obj, f"{field}_en")

# =============================ImplantTransplant ===========================
class SpecializationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Specialization
        fields = ["id", "name_en","name_ar"]
        
# ============================Hospital ======================================
class HospitalSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Hospital
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
            try:
                return request.build_absolute_uri(obj.image.url) if request else obj.image.url
            except:
                return None
        return None
 

class HospitalDetailSerializer(HospitalSerializer):
    specializations  = serializers.SerializerMethodField()
    Facilities  = serializers.SerializerMethodField()
    
    
    

    class Meta(HospitalSerializer.Meta):
        fields = HospitalSerializer.Meta.fields + ["Facilities", "specializations",]
        
    
    def get_specializations(self, obj):
        request = self.context.get("request")
        lang = self.context.get("lang", "en")

        specializations = obj.specializations.all() 

        return SpecializationSerializer(
            specializations,
            many=True,
            context={"request": request, "lang": lang}
        ).data
        


  