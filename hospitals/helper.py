from .models import Hospital,Specialization,Facilities
from .serializer import HospitalSerializer,HospitalDetailSerializer,SpecializationSerializer

def addHospitals(request):
    adminUser = request.user
    data = request.data

    name_en = data.get("name_en", None)
    name_ar = data.get("name_ar", None)
    
    description_en = data.get("description_en", None)
    description_ar = data.get("description_ar", None)
    
    
    image = request.FILES.get("image") 

    if not name_en or not name_ar or not description_en or not description_ar:
        return {
            "code": "400",
            "msg": "Bad request. Please ensure all required fields are provided",
        }
    if name_en and Hospital.getByName(name_en):
        return {"code": "SGN401", "msg": "Hospital already exists"}
    
    if name_en and Hospital.getByName(name_ar):
        return {"code": "SGN401", "msg": "Hospital already exists"}


    hospital = Hospital()
    hospital.name_ar = name_ar
    hospital.name_en = name_en
    hospital.description_ar = description_ar
    hospital.description_en = description_en
    hospital.image = image 

    hospital.save()

    data = {
        "code": "200",
        "msg": "Hospital Added successfully!",
    }
    return data


def listHospital(request):
    lang = request.GET.get("lang", "en")

    hospitals  = Hospital.objects.all()
    serializer  = HospitalSerializer(hospitals , many=True,context={"request": request, "lang": lang})

    return {"code": "200", "list": serializer.data}

def getHospitalDetail(request):
    data = request.GET
    lang = request.GET.get("lang", "en")
    
    hospital_id = data.get("hospital_id", None)
    
    if not hospital_id:
        return {
            "code": "404",
            "msg": "Bad request. Please ensure all required fields are provided.",
        }
        
    hospital = Hospital.objects.filter(id=hospital_id).first()
    if not hospital:
        return {"code": "401", "msg": "No record found with the provided ID."}

    serializer = HospitalDetailSerializer(
        hospital, context={"request": request,"lang": lang}
    )

    return {
        "code": "200",
        "data": serializer.data
    }

  

def updateHospital(request):
    data = request.data
    id = data.get("id", None)
    name_en = data.get("name_en", None)
    name_ar = data.get("name_ar", None)
    
    description_en = data.get("description_en", None)
    description_ar = data.get("description_ar", None)
    

    image = request.FILES.get("image") 
    
    if not id:
        return {
            "code": "400",
            "msg": "Bad request. Hospital ID is required to update.",
        }

    hospital  = Hospital.objects.filter(id=id).first()
    if not hospital :
        return {"code": "401", "msg": "No record found with the provided ID."}

    

    if name_en:
        hospital .name_en = name_en
    if name_ar:
        hospital .name_ar = name_ar
    if description_en:
        hospital .description_en = description_en
    if description_ar:
        hospital .description_ar = description_ar

    if image:
        hospital .image = image
    hospital .save()

    return {"code": "200", "msg": "Hospital Details updated successfully!"}


def deleteHospital(request):
    data = request.GET
    id = data.get("id", None)

    if not id:
        return {
            "code": "400",
            "msg": "Bad request. Please ensure all required fields are provided.",
        }

    hospital = Hospital.objects.filter(id=id).first()
    if not hospital:
        return {"code": "401", "msg": "No record found with the provided ID."}

    hospital.delete()
    return {"code": "200", "msg": "Hospital deleted successfully!"}

                
                # ==================================Specializations ====================================
                
      
def addSpecializations(request):
    data = request.data

    hospital_id = data.get("hospital_id")
    name_ar = data.get("name_ar", None)
    name_en = data.get("name_en", None)
    
    
    
    

    if not hospital_id or not name_ar or not name_en:
        return {
            "code": "400",
            "msg": "Bad request. Please ensure all required fields are provided",
        }

    # ✅ Get hospital safely
    try:
        hospital = Hospital.objects.get(id=hospital_id)
    except Hospital.DoesNotExist:
        return {
            
                "code": "404",
                "msg": "Hospital not found",
        
        }

    # ✅ Check duplicate
    if Specialization.objects.filter(
        name_en=name_en,
    ).exists():
        return  {
            "code": "409",
            "msg": "Specialization already exists for this hospital",
        },
       

    # ✅ Create specialization
    Specialization.objects.create(
        hospital=hospital,
        name_en=name_en,
        name_ar=name_ar,
     
    )

    return {
        "code": "200",
        "msg": "Specialization added successfully",
    },
    
    
def getSpecializationList(request):

    data = request.GET
    lang = data.get("lang", "en")   
    
    hospital_id = data.get("hospital_id", None)
    
    if not hospital_id:
        return {
            "code": "404",
            "msg": "Bad request. Please ensure all required fields are provided.",
        }
        
    hospital = Hospital.objects.filter(id=hospital_id).first()
    if not hospital:
        return {"code": "401", "msg": "No record found with the provided ID."}

    serializer = HospitalDetailSerializer(
        hospital, context={"request": request}
    )

    specializations  = Specialization.objects.filter(hospital_id=hospital_id)

    serializer = SpecializationSerializer(
        specializations, many=True,  context={"request": request, "lang": lang}   #

    )

    return {"code": "200", "list": serializer.data}


def updateSpecialization(request):
    data = request.data
    id = data.get("id", None)
    
    name_ar = data.get("name_ar", None)
    name_en = data.get("name_en", None)
    
  
    
    if not id:
        return {
            "code": "400",
            "msg": "Bad request. Please ensure all required fields are provided.",
        }

    specialization = Specialization.objects.filter(id=id).first()
    if not specialization:
        return {"code": "401", "msg": "No record found with the provided ID."}

    if name_en:
        specialization.name_en = name_en
    if name_ar:
        specialization.name_ar = name_ar
  
 
    specialization.save()

    return {"code": "200", "msg": "Specialization Details updated successfully!"}

def deleteSpecialization(request):
    data = request.GET
    id = data.get("id", None)

    if not id:
        return {
            "code": "400",
            "msg": "Bad request. Please ensure all required fields are provided.",
        }

    specializations = Specialization.objects.filter(id=id).first()
    if not specializations:
        return {"code": "401", "msg": "No record found with the provided ID."}

    specializations.delete()
    return {"code": "200", "msg": "specialization deleted successfully!"}


      # ==================================Facilities ====================================
                
      
def addFacilities(request):
    data = request.data

    hospital_id = data.get("hospital_id")
    name_ar = data.get("name_ar", None)
    name_en = data.get("name_en", None)
    
    
    
    

    if not hospital_id or not name_ar or not name_en:
        return {
            "code": "400",
            "msg": "Bad request. Please ensure all required fields are provided",
        }

    # ✅ Get hospital safely
    try:
        hospital = Hospital.objects.get(id=hospital_id)
    except Hospital.DoesNotExist:
        return {
            
                "code": "404",
                "msg": "Hospital not found",
        
        }

    # ✅ Check duplicate
    if Facilities.objects.filter(
        name_en=name_en,
    ).exists():
        return  {
            "code": "409",
            "msg": "Facilities already exists for this hospital",
        },
       

    # ✅ Create specialization
    Facilities.objects.create(
        hospital=hospital,
        name_en=name_en,
        name_ar=name_ar,
     
    )

    return {
        "code": "200",
        "msg": "Facilities added successfully",
    },
    
    
def getFacilitiesList(request):

    data = request.GET
    lang = data.get("lang", "en")   
    
    hospital_id = data.get("hospital_id", None)
    
    if not hospital_id:
        return {
            "code": "404",
            "msg": "Bad request. Please ensure all required fields are provided.",
        }
        
    hospital = Hospital.objects.filter(id=hospital_id).first()
    if not hospital:
        return {"code": "401", "msg": "No record found with the provided ID."}

    serializer = HospitalDetailSerializer(
        hospital, context={"request": request}
    )

    specializations  = Facilities.objects.filter(hospital_id=hospital_id)

    serializer = SpecializationSerializer(
        specializations, many=True,  context={"request": request, "lang": lang}   #

    )

    return {"code": "200", "list": serializer.data}


def updateFacilities(request):
    data = request.data
    id = data.get("id", None)
    
    name_ar = data.get("name_ar", None)
    name_en = data.get("name_en", None)
    
  
    
    if not id:
        return {
            "code": "400",
            "msg": "Bad request. Please ensure all required fields are provided.",
        }

    specialization = Facilities.objects.filter(id=id).first()
    if not specialization:
        return {"code": "401", "msg": "No record found with the provided ID."}

    if name_en:
        specialization.name_en = name_en
    if name_ar:
        specialization.name_ar = name_ar
  
 
    specialization.save()

    return {"code": "200", "msg": "Facilities Details updated successfully!"}

def deleteFacilities(request):
    data = request.GET
    id = data.get("id", None)

    if not id:
        return {
            "code": "400",
            "msg": "Bad request. Please ensure all required fields are provided.",
        }

    specializations = Facilities.objects.filter(id=id).first()
    if not specializations:
        return {"code": "401", "msg": "No record found with the provided ID."}

    specializations.delete()
    return {"code": "200", "msg": "Facilities deleted successfully!"}


