from .models import Hospital,Specialization,Facilities,Doctor,Procedure,HospitalImage
from .serializer import HospitalSerializer,HospitalDetailSerializer,SpecializationSerializer,DoctorSerializer,ProcedureSerializer

def addHospitals(request):
    adminUser = request.user
    data = request.data

    name_en = data.get("name_en", None)
    name_ar = data.get("name_ar", None)
    
    description_en = data.get("description_en", None)
    description_ar = data.get("description_ar", None)
    
    location_ar = data.get("location_ar", None)
    location_en = data.get("location_en", None)
    
    
    images = request.FILES.getlist("images")
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
    hospital.location_ar=location_ar
    hospital.location_en = location_en

    hospital.save()
    for image in images: 
        HospitalImage.objects.create(
            hospital=hospital,
            image=image
            )
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
    
    location_ar = data.get("location_ar", None)
    location_en = data.get("location_en", None)
    

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
    if location_en:
        hospital .location_en = location_en
    if location_ar:
        hospital .location_ar = location_ar
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


# ------------------------------Doctors --------------------------------------------
def addDoctor(request):
    data = request.data

    hospital_id = data.get("hospital_id")
    name_en = data.get("name_en")
    name_ar = data.get("name_ar")
    specialist_en = data.get("specialist_en")
    specialist_ar = data.get("specialist_ar")
    image = request.FILES.get("image")

    if not all([hospital_id, name_en, specialist_en]):
        return {
            "code": "400",
            "msg": "Please provide all required fields."
        }

    hospital = Hospital.objects.filter(id=hospital_id).first()
    if not hospital:
        return {
            "code": "404",
            "msg": "Hospital not found."
        }

    Doctor.objects.create(
        hospital=hospital,
        name_en=name_en,
        name_ar=name_ar,
        specialist_en=specialist_en,
        specialist_ar=specialist_ar,
        image=image
    )

    return {
        "code": "200",
        "msg": "Doctor added successfully."
    }

def getDoctorList(request):
    hospital_id = request.GET.get("hospital_id")
    lang = request.GET.get("lang", "en")

    doctors = Doctor.objects.filter(hospital_id=hospital_id)

    serializer = DoctorSerializer(
        doctors,
        many=True,
        context={"request": request, "lang": lang}
    )

    return {
        "code": "200",
        "list": serializer.data
    }

def updateDoctor(request):
    data = request.data

    doctor = Doctor.objects.filter(id=data.get("id")).first()

    if not doctor:
        return {
            "code": "404",
            "msg": "Doctor not found."
        }

    doctor.name_en = data.get("name_en", doctor.name_en)
    doctor.name_ar = data.get("name_ar", doctor.name_ar)
    doctor.specialist_en = data.get("specialist_en", doctor.specialist_en)
    doctor.specialist_ar = data.get("specialist_ar", doctor.specialist_ar)

    image = request.FILES.get("image")
    if image:
        doctor.image = image

    doctor.save()

    return {
        "code": "200",
        "msg": "Doctor updated successfully."
    }
def deleteDoctor(request):
    doctor = Doctor.objects.filter(id=request.GET.get("id")).first()

    if not doctor:
        return {
            "code": "404",
            "msg": "Doctor not found."
        }

    doctor.delete()

    return {
        "code": "200",
        "msg": "Doctor deleted successfully."
    }
    
# --------------------------PRocedure --------------------------------
def addProcedure(request):
    data = request.data

    hospital_id = data.get("hospital_id")
    name_en = data.get("name_en")
    name_ar = data.get("name_ar")
    description_en = data.get("description_en")
    description_ar = data.get("description_ar")
    image = request.FILES.get("image")

    if not all([hospital_id, name_en]):
        return {
            "code": "400",
            "msg": "Please provide all required fields."
        }

    hospital = Hospital.objects.filter(id=hospital_id).first()
    if not hospital:
        return {
            "code": "404",
            "msg": "Hospital not found."
        }

    Procedure.objects.create(
        hospital=hospital,
        name_en=name_en,
        name_ar=name_ar,
        description_en=description_en,
        description_ar=description_ar,
        image=image
    )

    return {
        "code": "200",
        "msg": "Procedure added successfully."
    }
def getProcedureList(request):
    hospital_id = request.GET.get("hospital_id")
    lang = request.GET.get("lang", "en")

    procedures = Procedure.objects.filter(hospital_id=hospital_id)

    serializer = ProcedureSerializer(
        procedures,
        many=True,
        context={"request": request, "lang": lang}
    )

    return {
        "code": "200",
        "list": serializer.data
    }
def updateProcedure(request):
    data = request.data

    procedure = Procedure.objects.filter(id=data.get("id")).first()

    if not procedure:
        return {
            "code": "404",
            "msg": "Procedure not found."
        }

    procedure.name_en = data.get("name_en", procedure.name_en)
    procedure.name_ar = data.get("name_ar", procedure.name_ar)
    procedure.description_en = data.get("description_en", procedure.description_en)
    procedure.description_ar = data.get("description_ar", procedure.description_ar)

    image = request.FILES.get("image")
    if image:
        procedure.image = image

    procedure.save()

    return {
        "code": "200",
        "msg": "Procedure updated successfully."
    }
    
def deleteProcedure(request):
    procedure = Procedure.objects.filter(id=request.GET.get("id")).first()

    if not procedure:
        return {
            "code": "404",
            "msg": "Procedure not found."
        }

    procedure.delete()

    return {
        "code": "200",
        "msg": "Procedure deleted successfully."
    }