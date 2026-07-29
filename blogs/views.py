from django.shortcuts import render
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from . import helper
from config.common.utils import makeResponse


class BlogAPIS(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = helper.saveBlogs(request)
        return makeResponse(data)
    
    
    def delete(self, request):
        data = helper.deleteBlog(request)
        return makeResponse(data)
    
    def put(self, request):
        data = helper.updateBlog(request)
        return makeResponse(data)
    
class BlogListAPIS(APIView):
    def get(self, request):
        data = helper.listBlogs(request)
        return makeResponse(data)
    
    
class BlogContentAPIS(APIView):
    def get(self, request):
        data = helper.getBlogContent(request)
        return makeResponse(data)

