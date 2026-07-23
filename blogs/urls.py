from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('blog-data/', views.BlogListAPIS.as_view(), name='blogs'),
    path('blogContent/', views.BlogAPIS.as_view(), name='singleBlog'),
    path('list/', views.BlogListUNSECURES.as_view(), name='blogData'),
    
    
  

]
