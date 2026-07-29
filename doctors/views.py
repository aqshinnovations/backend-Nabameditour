from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from . import helper
from config.common.utils import makeResponse
    # --------------------------------------Category ------------------------------------------------------


class CategoriesAPIS(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        data = helper.addCategory(request)
        return makeResponse(data)
    
    def get(self, request):
        data = helper.listCategory(request)
        return makeResponse(data)
    
    def put(self, request):
        data = helper.updateCategory(request)
        return makeResponse(data)
    
    def delete(self, request):
        data = helper.deleteCategory(request)
        return makeResponse(data)

# class HospitalDetailsAPIS(APIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]
    
#     def get(self, request):
#         data = helper.getHospitalDetail(request)
#         return makeResponse(data)
    # --------------------------------------Doctors ------------------------------------------------------
class DoctorsAPIS(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        data = helper.addDoctors(request)
        return makeResponse(data)
    
    def get(self, request):
        data = helper.getDoctorsList(request)
        return makeResponse(data)
    
    def put(self, request):
        data = helper.updateDoctors(request)
        return makeResponse(data)
    
    def delete(self, request):
        data = helper.deleteDoctors(request)
        return makeResponse(data)
    
