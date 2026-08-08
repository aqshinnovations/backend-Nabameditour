from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from . import helper
from config.common.utils import makeResponse
# Create your views here.

# class PatientsAPI(APIView):
#     # authentication_classes = [JWTAuthentication]
#     # permission_classes = [IsAuthenticated]

#     def post(self, request):
#         data = helper.savePatients(request)
#         return makeResponse(data)
    
#     def get(self, request):
#         data = helper.listPatients(request)
#         return makeResponse(data)
    
#     def delete(self, request):
#         data = helper.deletePatients(request)
#         return makeResponse(data)
class PatientsAPI(APIView):
    # POST → No token required

    def post(self, request):
        data = helper.savePatients(request)
        return makeResponse(data)


class PatientsListAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = helper.listPatients(request)
        return makeResponse(data)

    def delete(self, request):
        data = helper.deletePatients(request)
        return makeResponse(data)
        
class PatientReportDownloadAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        response = helper.downloadPatientReport(request)
        
        if isinstance(response, dict):
            return makeResponse(response)
        return response