from rest_framework import serializers
from .models import (
    Hospital,
    Specialization,
    Facilities,
    Doctor,
    Procedure,
    HospitalImage,
    GovernmentSchemeLogo,
)


class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = ["id", "name_en", "name_ar"]


class FacilitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Facilities
        fields = ["id", "name_en", "name_ar"]


class DoctorSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Doctor
        fields = [
            "id",
            "name_en",
            "name_ar",
            "specialist_en",
            "specialist_ar",
            "image",
        ]

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image:
            return (
                request.build_absolute_uri(obj.image.url) if request else obj.image.url
            )
        return None


class ProcedureSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Procedure
        fields = [
            "id",
            "name_en",
            "name_ar",
            "description_en",
            "description_ar",
            "image",
        ]

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image:
            return (
                request.build_absolute_uri(obj.image.url) if request else obj.image.url
            )
        return None


class HospitalImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = HospitalImage
        fields = [
            "id",
            "image",
        ]

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image:
            return (
                request.build_absolute_uri(obj.image.url) if request else obj.image.url
            )
        return None


class GovtSchemeSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = GovernmentSchemeLogo
        fields = [
            "id",
            "image",
        ]

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image:
            return (
                request.build_absolute_uri(obj.image.url) if request else obj.image.url
            )
        return None


class HospitalSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    government_scheme_logos = serializers.SerializerMethodField()
    specializations = serializers.SerializerMethodField()
    facilities = serializers.SerializerMethodField()
    doctors = serializers.SerializerMethodField()
    procedures = serializers.SerializerMethodField()
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
            "location_ar",
            "location_en",
            "images",
            "specializations",
            "facilities",
            "doctors",
            "procedures",
            "government_scheme_logos",
            "created_at",
            "updated_at",
        ]

    def get_images(self, obj):
        return HospitalImageSerializer(
            obj.images.all(), many=True, context=self.context
        ).data

    def get_government_scheme_logos(self, obj):
        return GovtSchemeSerializer(
            obj.government_scheme_logos.all(),
            many=True,
            context=self.context,
        ).data

    def get_specializations(self, obj):
        return SpecializationSerializer(obj.specializations.all()[:3], many=True).data

    def get_facilities(self, obj):
        return FacilitiesSerializer(
            obj.Facilities.all()[
                :3
            ],  # change to obj.facilities.all() if related_name="facilities"
            many=True,
        ).data

    def get_doctors(self, obj):
        return DoctorSerializer(
            obj.doctors.all()[:3], many=True, context=self.context
        ).data

    def get_procedures(self, obj):
        return ProcedureSerializer(
            obj.procedures.all()[:3], many=True, context=self.context
        ).data


class HospitalDetailSerializer(HospitalSerializer):
    specializations = SpecializationSerializer(many=True, read_only=True)
    facilities = FacilitiesSerializer(
        source="Facilities",  # remove source if related_name="facilities"
        many=True,
        read_only=True,
    )
    doctors = DoctorSerializer(many=True, read_only=True)

    procedures = ProcedureSerializer(many=True, read_only=True)

    class Meta(HospitalSerializer.Meta):
        fields = HospitalSerializer.Meta.fields
