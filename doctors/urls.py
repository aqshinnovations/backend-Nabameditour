from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('category/', views.CategoriesAPIS.as_view(), name='hospitals'),
    # path('HospitalDetailsAPIS/', views.HospitalDetailsAPIS.as_view(), name='HospitalDetailsAPIS'),
    
    path('doctors/', views.DoctorsAPIS.as_view(), name='departments'),
  
    
    
    
    
    
    
  

]
