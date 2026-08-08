from rest_framework import serializers
from datetime import datetime
from django.conf import settings

from django.utils.timezone import now
from .models import (
    Patients
  
)

class PatientsSerializer(serializers.ModelSerializer):
    report = serializers.SerializerMethodField()
    created = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    updated = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    class Meta:
        model = Patients
        fields = [
            "id",
            "name",
            "email",
            "mobile",
            "aboutHealth",
            "report",
            "created",    
            "updated",
       
        ]
    def get_report(self, obj):
        request = self.context.get("request")
        if obj.report and hasattr(obj.report, "url"):
            return request.build_absolute_uri(obj.report.url)
        return None

