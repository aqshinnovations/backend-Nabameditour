from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
  
    path('hospitals/', views.HospitalAPIS.as_view(), name='hospitals'),
    path('HospitalDetailsAPIS/', views.HospitalDetailsAPIS.as_view(), name='HospitalDetailsAPIS'),
    path('specializations/', views.SpecializationAPIS.as_view(), name='specializations'),
    path('Facilities/', views.FacilitiesAPIS.as_view(), name='facilities'),
    
    
    

    

]
