from rest_framework import serializers
from .models import Hospital, Specialization, Facilities


class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = ["id", "name_en", "name_ar"]


class FacilitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Facilities
        fields = ["id", "name_en", "name_ar"]


class HospitalSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    specializations = serializers.SerializerMethodField()
    facilities = serializers.SerializerMethodField()

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
            "specializations",
            "facilities",
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

    def get_specializations(self, obj):
        return SpecializationSerializer(
            obj.specializations.all()[:3],
            many=True
        ).data

    def get_facilities(self, obj):
        return FacilitiesSerializer(
            obj.Facilities.all()[:3],   # change to obj.facilities.all() if related_name="facilities"
            many=True
        ).data


class HospitalDetailSerializer(HospitalSerializer):
    specializations = SpecializationSerializer(many=True, read_only=True)
    facilities = FacilitiesSerializer(
        source="Facilities",   # remove source if related_name="facilities"
        many=True,
        read_only=True,
    )

    class Meta(HospitalSerializer.Meta):
        fields = HospitalSerializer.Meta.fields