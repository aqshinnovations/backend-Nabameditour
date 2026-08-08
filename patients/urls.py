from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('patients-report/', views.PatientReportDownloadAPI.as_view(), name='patients-report'),
    path("patients/", views.PatientsAPI.as_view(), name="patients"),
    path("patients/list/", views.PatientsListAPI.as_view(), name="patients-list"),

]
#add media file root and url
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
