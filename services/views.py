from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from . import helper
from config.common.utils import makeResponse
# Create your views here.
    # --------------------------------------Services ------------------------------------------------------
class ServicesList(APIView):
    def get(self, request):
        data = helper.getServicesList(request)
        return makeResponse(data)
class ServicesAPIS(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = helper.addServices(request)
        return makeResponse(data)
    
    def put(self, request):
        data = helper.updateServices(request)
        return makeResponse(data)
    
    def delete(self, request):
        data = helper.deleteServices(request)
        return makeResponse(data)
    