from django.shortcuts import render
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from . import helper
from config.common.utils import makeResponse


class HospitalList(APIView):
    def get(self, request):
        data = helper.listHospital(request)
        return makeResponse(data)
class HospitalAPIS(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = helper.addHospitals(request)
        return makeResponse(data)
    
    
    def put(self, request):
        data = helper.updateHospital(request)
        return makeResponse(data)
    
    def delete(self, request):
        data = helper.deleteHospital(request)
        return makeResponse(data)

class HospitalDetailsAPIS(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    
    def get(self, request):
        data = helper.getHospitalDetail(request)
        return makeResponse(data)


# -------------------------------  Specialization  --------------------------------------
    
class SpecializationAPIS(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = helper.addSpecializations(request)
        return makeResponse(data)
    
    def get(self, request):
        data = helper.getSpecializationList(request)
        return makeResponse(data)
    
    def put(self, request):
        data = helper.updateSpecialization(request)
        return makeResponse(data)
    
    def delete(self, request):
        data = helper.deleteSpecialization(request)
        return makeResponse(data)
    
# -------------------------------  Facilities  --------------------------------------

class FacilitiesAPIS(APIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]

    def post(self, request):
        data = helper.addFacilities(request)
        return makeResponse(data)
    
    def get(self, request):
        data = helper.getFacilitiesList(request)
        return makeResponse(data)
    
    def put(self, request):
        data = helper.updateFacilities(request)
        return makeResponse(data)
    
    def delete(self, request):
        data = helper.deleteFacilities(request)
        return makeResponse(data)
# ------------------------------- Doctors --------------------------------------

class DoctorAPIS(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = helper.addDoctor(request)
        return makeResponse(data)

    def get(self, request):
        data = helper.getDoctorList(request)
        return makeResponse(data)

    def put(self, request):
        data = helper.updateDoctor(request)
        return makeResponse(data)

    def delete(self, request):
        data = helper.deleteDoctor(request)
        return makeResponse(data)


# ------------------------------- Procedures --------------------------------------

class ProcedureAPIS(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = helper.addProcedure(request)
        return makeResponse(data)

    def get(self, request):
        data = helper.getProcedureList(request)
        return makeResponse(data)

    def put(self, request):
        data = helper.updateProcedure(request)
        return makeResponse(data)

    def delete(self, request):
        data = helper.deleteProcedure(request)
        return makeResponse(data)