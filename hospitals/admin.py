from django.contrib import admin
from .models import (
   Hospital,Specialization,Facilities
)


admin.site.register(
    [
       Hospital,Specialization,Facilities
    ]
)