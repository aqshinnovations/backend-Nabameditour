from django.shortcuts import render
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from . import helper
from config.common.utils import makeResponse


class BlogListAPIS(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = helper.saveBlogs(request)
        return makeResponse(data)
    
    def get(self, request):
        data = helper.listBlogs(request)
        return makeResponse(data)
    


    def delete(self, request):
        data = helper.deleteBlog(request)
        return makeResponse(data)
    
    def put(self, request):
        data = helper.updateBlog(request)
        return makeResponse(data)
    
class BlogAPIS(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    
    def get(self, request):
        data = helper.listSingleBlog(request)
        return makeResponse(data)

class BlogListUNSECURES(APIView):
    def get(self, request):
        data = helper.listBlogs(request)
        return makeResponse(data)