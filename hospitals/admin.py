from django.contrib import admin
from .models import (
    Hospital,
    Specialization,
    Facilities,
    HospitalImage,
    GovernmentSchemeLogo,
)

admin.site.register(
    [Hospital, Specialization, Facilities, HospitalImage, GovernmentSchemeLogo]
)
