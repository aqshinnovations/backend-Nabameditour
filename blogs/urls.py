from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('blog/', views.BlogAPIS.as_view(), name='blogData'),
    path('list/', views.BlogListAPIS.as_view(), name='blogData'),
    path('blog-data/', views.BlogContentAPIS.as_view(), name='blogs'),
    
    
  

]
