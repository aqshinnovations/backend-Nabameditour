from django.urls import path

from .views import TestimonialsList, TestimonialsAPIS


urlpatterns = [
    path(
        "testimonials/list",
        TestimonialsList.as_view(),
        name="testimonials-list",
    ),

    path(
        "testimonials/",
        TestimonialsAPIS.as_view(),
        name="testimonials-api",
    ),
]