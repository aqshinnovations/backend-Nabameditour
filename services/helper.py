from .models import Services
from .serializer import ServicesSerializer
from django.db.models import Q


                # ==================================Services ====================================        
      
def addServices(request):
    data = request.data

    name_ar = data.get("name_ar", None)
    name_en = data.get("name_en", None)
    
    description_ar = data.get("description_ar", None)
    description_en = data.get("description_en", None)
    
    image = request.FILES.get("image")


    if  not name_ar or not name_en  or not description_en or not description_ar:
        return {
            "code": "400",
            "msg": "Bad request. Please ensure all required fields are provided",
        }


    if Services.objects.filter( name_en=name_en).exists():
        return {
            "code": "409",
            "msg": "Services already exists",
        }
    services = Services()
    services.name_ar = name_ar
    services.name_en = name_en
    services.description_ar = description_ar
    services.description_en = description_en

    services.image = image
     
    services.save()

    return {
        "code": "200",
          "msg": "Services added successfully",
    },
    
def getServicesList(request):
    services = Services.objects.all()

    serializer = ServicesSerializer(
        services,
        many=True,
        context={"request": request},
    )

    return {
        "code": "200",
        "list": serializer.data,
    }
    
def updateServices(request):
    data = request.data
    id = data.get("id", None)
    
    name_ar = data.get("name_ar", None)
    name_en = data.get("name_en", None)
    
    description_en = data.get("description_en", None)
    description_ar = data.get("description_ar", None)
    
   
    image = request.FILES.get("image")
  
    
    if not id:
        return {
            "code": "400",
            "msg": "Bad request. Please ensure all required fields are provided.",
        }

    services = Services.objects.filter(id=id).first()
    if not services:
        return {"code": "401", "msg": "No record found with the provided ID."}

    if name_en:
        services.name_en = name_en
    if name_ar:
        services.name_ar = name_ar

    if description_en:
        services.description_en = description_en
    if description_ar:
        services.description_ar = description_ar

    if image:
     services.image = image
 
    services.save()

    return {"code": "200", "msg": "Services Details updated successfully!"}

def deleteServices(request):
    data = request.GET
    id = data.get("id", None)

    if not id:
        return {
            "code": "400",
            "msg": "Bad request. Please ensure all required fields are provided.",
        }

    services = Services.objects.filter(id=id).first()
    if not services:
        return {"code": "401", "msg": "No record found with the provided ID."}

    services.delete()
    return {"code": "200", "msg": "Services deleted successfully!"}



