from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from . import helper
from config.common.utils import makeResponse


# ================================== Testimonials ====================================


class TestimonialsList(APIView):

    def get(self, request):
        data = helper.getTestimonialsList(request)
        return makeResponse(data)


class TestimonialsAPIS(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = helper.addTestimonials(request)
        return makeResponse(data)



    def delete(self, request):
        data = helper.deleteTestimonials(request)
        return makeResponse(data)