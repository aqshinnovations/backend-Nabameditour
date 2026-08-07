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


    # --------------------------------------Doctors ------------------------------------------------------
class DoctorsList(APIView):
    def get(self, request):
        data = helper.getDoctorsList(request)
        return makeResponse(data)
class DoctorsAPIS(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = helper.addDoctors(request)
        return makeResponse(data)
    
    def put(self, request):
        data = helper.updateDoctors(request)
        return makeResponse(data)
    
    def delete(self, request):
        data = helper.deleteDoctors(request)
        return makeResponse(data)
    
class DoctorsDetailsAPIS(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    
    def get(self, request):
        data = helper.getDoctorsDetail(request)
        return makeResponse(data)
# -------------------------------------- Qualification ------------------------------------------------------

class QualificationListAPI(APIView):
    # Public API
    def get(self, request):
        data = helper.getQualificationList(request)
        return makeResponse(data)


class QualificationAPIS(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = helper.addQualification(request)
        return makeResponse(data)

    def put(self, request):
        data = helper.updateQualification(request)
        return makeResponse(data)

    def delete(self, request):
        data = helper.deleteQualification(request)
        return makeResponse(data)


# -------------------------------------- Specialist ------------------------------------------------------

class SpecialistListAPI(APIView):
    # Public API
    def get(self, request):
        data = helper.getSpecialistList(request)
        return makeResponse(data)


class SpecialistAPIS(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = helper.addSpecialist(request)
        return makeResponse(data)

    def put(self, request):
        data = helper.updateSpecialist(request)
        return makeResponse(data)

    def delete(self, request):
        data = helper.deleteSpecialist(request)
        return makeResponse(data)
    
# -------------------------------------- Award ------------------------------------------------------

class AwardsListAPI(APIView):
    # Public API
    def get(self, request):
        data = helper.getAwardsList(request)
        return makeResponse(data)


class AwardsAPIS(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = helper.addAward(request)
        return makeResponse(data)

    def put(self, request):
        data = helper.updateAward(request)
        return makeResponse(data)

    def delete(self, request):
        data = helper.deleteAward(request)
        return makeResponse(data)
# -------------------------------------- Images ------------------------------------------------------

class ImageListAPI(APIView):
    # Public API
    def get(self, request):
        data = helper.getImageList(request)
        return makeResponse(data)


class ImageAPIS(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = helper.addImage(request)
        return makeResponse(data)

    def put(self, request):
        data = helper.updateImage(request)
        return makeResponse(data)

    def delete(self, request):
        data = helper.deleteImage(request)
        return makeResponse(data)