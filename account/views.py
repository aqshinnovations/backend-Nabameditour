from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from . import helper
from config.common.utils import makeResponse
from rest_framework.permissions import IsAuthenticated
from django.http import FileResponse
import os
from django.conf import settings
from .models import  BlacklistedToken
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed

from rest_framework import viewsets
from rest_framework import status


def check_blacklisted_token(request):
    token = request.auth
    if token and BlacklistedToken.objects.filter(token=token).exists():
        raise AuthenticationFailed("Token is blacklisted")


class AccountSignInApi(APIView):
    def post(self, request):
        data = helper.signInAccount(request)
        return makeResponse(data)


# logout
class AccountLogout(APIView):
    def post(self, request):
        data = helper.logout_user(request)
        return makeResponse(data)


class AccountSignUpApi(APIView):
    def post(self, request):
        data = helper.signUpAccount(request)
        return makeResponse(data)


class ProfileApi(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        check_blacklisted_token(request)
        data = helper.getAccountProfile(request)
        return makeResponse(data)


class MembersApi(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        check_blacklisted_token(request)
        data = helper.listMembrs(request)
        return makeResponse(data)

    def post(self, request):
        print(f"Authenticated user: {request.user.username}")
        check_blacklisted_token(request)
        data = helper.addMember(request)
        return makeResponse(data)
    
    def delete(self, request):
        data = helper.deleteMember(request)
        return makeResponse(data)


class UpdateMemberApi(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        check_blacklisted_token(request)
        data = helper.updateMember(request)
        return makeResponse(data)


class ActivateMemberApi(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        check_blacklisted_token(request)
        data = helper.activateMember(request)
        return makeResponse(data)


class DeleteMemberApi(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        check_blacklisted_token(request)
        data = helper.deleteMember(request)
        return makeResponse(data)

class ChangePassword(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = helper.changePassword(request)
        return makeResponse(data)
