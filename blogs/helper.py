from .models import Blogs
from .serializers import BlogsSerializer

def saveBlogs(request):
    adminUser = request.user
    data = request.data

    title = data.get("title", None)
    content = data.get("content", None)
    author = data.get("author", None)
    cover_image = request.FILES.get("cover_image") 

    if not title or not content or not author:
        return {
            "code": "400",
            "msg": "Bad request. Please ensure all required fields are provided",
        }

    blogsDetails = Blogs()
    blogsDetails.title = title
    blogsDetails.content = content
    blogsDetails.author = author
    blogsDetails.cover_image = cover_image 

    blogsDetails.save()

    data = {
        "code": "200",
        "msg": "Blog Saved successfully!",
    }
    return data


def listBlogs(request):
    blogsList = Blogs.objects.all()
    blogsSerializer = BlogsSerializer(blogsList, many=True, context={"request": request})

    return {"code": "200", "list": blogsSerializer.data}


def listSingleBlog(request):
    data = request.GET
    
    id = data.get("id", None)
    
    if not id:
        return {
            "code": "400",
            "msg": "Bad request. Please ensure all required fields are provided.",
        }
    blog = Blogs.objects.get(id=id)
    blogSerializer = BlogsSerializer(blog, context={"request": request})

    return {"code": "200", "list": blogSerializer.data}


def deleteBlog(request):
    data = request.GET
    id = data.get("id", None)

    if not id:
        return {
            "code": "400",
            "msg": "Bad request. Please ensure all required fields are provided.",
        }

    blog = Blogs.objects.filter(id=id).first()
    if not blog:
        return {"code": "401", "msg": "No record found with the provided ID."}

    blog.delete()
    return {"code": "200", "msg": "Blog Data deleted successfully!"}

def updateBlog(request):
    data = request.data
    id = data.get("id", None)
    title = data.get("title", None)
    content = data.get("content",None)
    author = data.get("author", None)    
    cover_image = request.FILES.get("cover_image") 
    
    if not id:
        return {
            "code": "400",
            "msg": "Bad request. Blog ID is required to update.",
        }

    blog = Blogs.objects.filter(id=id).first()
    if not blog:
        return {"code": "401", "msg": "No record found with the provided ID."}

    

    if title:
        blog.title = title
    if content:
        blog.content = content
    if author:
        blog.author = author
    if cover_image:
        blog.cover_image = cover_image

    blog.save()

    return {"code": "200", "msg": "Blog updated successfully!"}