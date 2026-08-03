from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('services/', views.ServicesAPIS.as_view(), name='departments'),
    path('list/', views.ServicesList.as_view(), name='departments'),

]
