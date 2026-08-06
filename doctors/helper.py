from .models import Category,Doctor,Qualification,Specialist,Awards,Images
from .serializer import CategoriesSerializer,DoctorsSerializer,DoctorsDetailSerializer,QualificationSerializer,SpecialistSerializer,AwardSerializer,ImageSerializer
from django.db.models import Q
                # ==================================category ====================================

def addCategory(request):
    adminUser = request.user
    data = request.data

    name_en = data.get("name_en", None)
    name_ar = data.get("name_ar", None)

    if not name_en or not name_ar :
        return {
            "code": "400",
            "msg": "Bad request. Please ensure all required fields are provided",
        }
    if name_en and Category.get_by_name(name_en):
        return {"code": "SGN401", "msg": "Category already exists"}
    

    category = Category()
    category.name_ar = name_ar
    category.name_en = name_en
    category.save()

    data = {
        "code": "200",
        "msg": "category Added successfully!",
    }
    return data


def listCategory(request):
    lang = request.GET.get("lang", "en")

    categories  = Category.objects.all()
    serializer  = CategoriesSerializer(categories , many=True,context={"request": request, "lang": lang})

    return {"code": "200", "list": serializer.data}


def updateCategory(request):
    data = request.data
    id = data.get("id", None)
    name_en = data.get("name_en", None)
    name_ar = data.get("name_ar", None)
    
        
    if not id:
        return {
            "code": "400",
            "msg": "Bad request. category ID is required to update.",
        }

    category  = Category.objects.filter(id=id).first()
    if not category :
        return {"code": "401", "msg": "No record found with the provided ID."}

    if name_en:
        category .name_en = name_en
    if name_ar:
        category .name_ar = name_ar
   
    category .save()
    return {"code": "200", "msg": "category updated successfully!"}


def deleteCategory(request):
    data = request.GET
    id = data.get("id", None)

    if not id:
        return {
            "code": "400",
            "msg": "Bad request. Please ensure all required fields are provided.",
        }

    category = Category.objects.filter(id=id).first()
    if not category:
        return {"code": "401", "msg": "No record found with the provided ID."}

    category.delete()
    return {"code": "200", "msg": "category deleted successfully!"}

                
                # ================================== Doctors ====================================
                
      
def addDoctors(request):
    data = request.data

    category_id = data.get("category_id")
    name_ar = data.get("name_ar", None)
    name_en = data.get("name_en", None)
    
    about_ar = data.get("about_ar", None)
    about_en = data.get("about_en", None)
    
    experience_ar = data.get("experience_ar", None)
    experience_en = data.get("experience_en", None)
    
    qualification_ar = data.get("qualification_ar", None)
    qualification_en = data.get("qualification_en", None)
    
    specialist_ar = data.get("specialist_ar", None)
    specialist_en = data.get("specialist_en", None)
    
    position_ar = data.get("position_ar", None)
    position_en = data.get("position_en", None)

    image = request.FILES.get("image")


    if not category_id or not name_ar or not name_en :
        return {
            "code": "400",
            "msg": "Bad request. Please ensure all required fields are provided",
        }

    # ✅ Get hospital safely
    try:
        category = Category.objects.get(id=category_id)
    except category.DoesNotExist:
        return {
            
                "code": "404",
                "msg": "Category not found",
        
        }
    if Doctor.objects.filter(category=category, name_en=name_en).exists():
        return {
            "code": "409",
            "msg": "Doctor already exists",
        }
    doctors = Doctor()
    doctors.name_ar = name_ar
    doctors.name_en = name_en
    doctors.about_ar = about_ar
    doctors.about_en = about_en
    doctors.experience_ar = experience_ar
    doctors.experience_en = experience_en
    doctors.qualification_ar = qualification_ar
    doctors.qualification_en = qualification_en
    doctors.specialist_ar = specialist_ar
    doctors.specialist_en = specialist_en
    doctors.image = image
    doctors.category = category  
    doctors.position_ar = position_ar
    doctors.position_en= position_en
     
    doctors.save()

    return {
        "code": "200",
          "msg": "Doctors added successfully",
    },
    
def getDoctorsList(request):
    data = request.GET
    lang = data.get("lang", "en")
    category_id = data.get("category_id")

    if not category_id:
        return {
            "code": "400",
            "msg": "Please provide category_id.",
        }

    doctors = Doctor.objects.filter(category_id=category_id)

    serializer = DoctorsSerializer(
        doctors,
        many=True,
        context={"request": request, "lang": lang},
    )

    return {
        "code": "200",
        "list": serializer.data,
    }
    
    # --------------------
    
    
def getDoctorsDetail(request):
    data = request.GET
    lang = request.GET.get("lang", "en")
    
    id = data.get("id", None)
    
    if not id:
        return {
            "code": "404",
            "msg": "Bad request. Please ensure all required fields are provided.",
        }
        
    hospital = Doctor.objects.filter(id=id).first()
    if not hospital:
        return {"code": "401", "msg": "No record found with the provided ID."}

    serializer = DoctorsDetailSerializer(
        hospital, context={"request": request,"lang": lang}
    )

    return {
        "code": "200",
        "data": serializer.data
    }

  
    # =================
def updateDoctors(request):
    data = request.data
    id = data.get("id", None)
    
    name_ar = data.get("name_ar", None)
    name_en = data.get("name_en", None)
    
    about_ar = data.get("about_ar", None)
    about_en = data.get("about_en", None)
    
    experience_ar = data.get("experience_ar", None)
    experience_en = data.get("experience_en", None)
    
    qualification_ar = data.get("qualification_ar", None)
    qualification_en = data.get("qualification_en", None)
    
    specialist_ar = data.get("specialist_ar", None)
    specialist_en = data.get("specialist_en", None)
    
    position_ar = data.get("position_ar", None)
    position_en = data.get("position_en", None)

    image = request.FILES.get("image")
  
    
    if not id:
        return {
            "code": "400",
            "msg": "Bad request. Please ensure all required fields are provided.",
        }

    doctor = Doctor.objects.filter(id=id).first()
    if not doctor:
        return {"code": "401", "msg": "No record found with the provided ID."}

    if name_en:
        doctor.name_en = name_en
    if name_ar:
        doctor.name_ar = name_ar

    if about_ar:
        doctor.about_ar = about_ar
    if about_en:
        doctor.about_en = about_en


    if experience_ar:
        doctor.experience_ar = experience_ar
    if experience_en:
        doctor.experience_en = experience_en
        

    if qualification_ar:
        doctor.qualification_ar = qualification_ar
    if qualification_en:
        doctor.qualification_en = qualification_en
        

    if specialist_ar:
        doctor.specialist_ar = specialist_ar
    if specialist_en:
        doctor.specialist_en = specialist_en
        
    if position_ar:
            doctor.position_ar = position_ar
    if position_en:
            doctor.position_en = position_en
        
    if image:
     doctor.image = image
 
    doctor.save()

    return {"code": "200", "msg": "Doctors Details updated successfully!"}

def deleteDoctors(request):
    data = request.GET
    id = data.get("id", None)

    if not id:
        return {
            "code": "400",
            "msg": "Bad request. Please ensure all required fields are provided.",
        }

    doctor = Doctor.objects.filter(id=id).first()
    if not doctor:
        return {"code": "401", "msg": "No record found with the provided ID."}

    doctor.delete()
    return {"code": "200", "msg": "Doctor deleted successfully!"}




# ------------------qua;ification -------------------

def addQualification(request):
    data = request.data

    doctor_id = data.get("doctor_id")
    name_en = data.get("name_en")
    name_ar = data.get("name_ar")

    if not doctor_id or not name_en:
        return {
            "code": "400",
            "msg": "doctor_id and name_en are required."
        }

    doctor = Doctor.objects.filter(id=doctor_id).first()
    if not doctor:
        return {
            "code": "404",
            "msg": "Doctor not found."
        }
    if Qualification.objects.filter(
    doctor=doctor
    ).filter(
        Q(name_en__iexact=name_en) |
        Q(name_ar__iexact=name_ar)
    ).exists():
        return {
            "code": "409",
            "msg": "Qualification already exists."
        }

    return {
        "code": "200",
        "msg": "Qualification added successfully."
    }

def getQualificationList(request):
    doctor_id = request.GET.get("doctor_id")

    if not doctor_id:
        return {
            "code": "400",
            "msg": "doctor_id is required."
        }

    qualifications = Qualification.objects.filter(doctor_id=doctor_id)

    serializer = QualificationSerializer(
        qualifications,
        many=True
    )

    return {
        "code": "200",
        "list": serializer.data
    }
def updateQualification(request):
    data = request.data

    id = data.get("id")
    name_en = data.get("name_en")
    name_ar = data.get("name_ar")

    qualification = Qualification.objects.filter(id=id).first()

    if not qualification:
        return {
            "code": "404",
            "msg": "Qualification not found."
        }

    if name_en:
        qualification.name_en = name_en

    if name_ar:
        qualification.name_ar = name_ar

    qualification.save()

    return {
        "code": "200",
        "msg": "Qualification updated successfully."
    }
def deleteQualification(request):
    id = request.GET.get("id")

    qualification = Qualification.objects.filter(id=id).first()

    if not qualification:
        return {
            "code": "404",
            "msg": "Qualification not found."
        }

    qualification.delete()

    return {
        "code": "200",
        "msg": "Qualification deleted successfully."
    }
    
    # =================speciliast====================

def addSpecialist(request):
    data = request.data

    doctor_id = data.get("doctor_id")
    name_en = data.get("name_en")
    name_ar = data.get("name_ar")

    if not doctor_id or not name_en:
        return {
            "code": "400",
            "msg": "doctor_id and name_en are required."
        }

    doctor = Doctor.objects.filter(id=doctor_id).first()

    if not doctor:
        return {
            "code": "404",
            "msg": "Doctor not found."
        }
    if Specialist.objects.filter(
        doctor=doctor
        ).filter(
            Q(name_en__iexact=name_en) |
            Q(name_ar__iexact=name_ar)
        ).exists():
            return {
                "code": "409",
                "msg": "Specialist already exists."
            }
    Specialist.objects.create(
        doctor=doctor,
        name_en=name_en,
        name_ar=name_ar
    )

    return {
        "code": "200",
        "msg": "Specialist added successfully."
    } 
    
def getSpecialistList(request):
    doctor_id = request.GET.get("doctor_id")

    if not doctor_id:
        return {
            "code": "400",
            "msg": "doctor_id is required."
        }

    specialists = Specialist.objects.filter(
        doctor_id=doctor_id
    )

    serializer = SpecialistSerializer(
        specialists,
        many=True
    )

    return {
        "code": "200",
        "list": serializer.data
    }
    
def updateSpecialist(request):
    data = request.data

    id = data.get("id")
    name_en = data.get("name_en")
    name_ar = data.get("name_ar")

    specialist = Specialist.objects.filter(id=id).first()

    if not specialist:
        return {
            "code": "404",
            "msg": "Specialist not found."
        }

    if name_en:
        specialist.name_en = name_en

    if name_ar:
        specialist.name_ar = name_ar

    specialist.save()

    return {
        "code": "200",
        "msg": "Specialist updated successfully."
    } 
    
def deleteSpecialist(request):
    id = request.GET.get("id")

    specialist = Specialist.objects.filter(id=id).first()

    if not specialist:
        return {
            "code": "404",
            "msg": "Specialist not found."
        }

    specialist.delete()

    return {
        "code": "200",
        "msg": "Specialist deleted successfully."
    }
    
    
      # =================awards====================
    
def addAward(request):
        data = request.data
    
        doctor_id = data.get("doctor_id")
        name_en = data.get("name_en")
        name_ar = data.get("name_ar")
    
        if not doctor_id or not name_en:
            return {
                "code": "400",
                "msg": "doctor_id and name_en are required."
            }
    
        doctor = Doctor.objects.filter(id=doctor_id).first()
    
        if not doctor:
            return {
                "code": "404",
                "msg": "Doctor not found."
            }
        if Awards.objects.filter(
            doctor=doctor
            ).filter(
                Q(name_en__iexact=name_en) |
                Q(name_ar__iexact=name_ar)
            ).exists():
                return {
                    "code": "409",
                    "msg": "Award already exists."
                }
        Awards.objects.create(
            doctor=doctor,
            name_en=name_en,
            name_ar=name_ar
        )
    
        return {
            "code": "200",
            "msg": "Award added successfully."
        } 
        
def getAwardsList(request):
        doctor_id = request.GET.get("doctor_id")
    
        if not doctor_id:
            return {
                "code": "400",
                "msg": "doctor_id is required."
            }
    
        awards = Awards.objects.filter(
            doctor_id=doctor_id
        )
    
        serializer = AwardSerializer(
            awards,
            many=True
        )
    
        return {
            "code": "200",
            "list": serializer.data
        }
        
def updateAward(request):
        data = request.data
    
        id = data.get("id")
        name_en = data.get("name_en")
        name_ar = data.get("name_ar")
    
        awards = Awards.objects.filter(id=id).first()
    
        if not awards:
            return {
                "code": "404",
                "msg": "Award not found."
            }
    
        if name_en:
            awards.name_en = name_en
    
        if name_ar:
            awards.name_ar = name_ar
    
        awards.save()
    
        return {
            "code": "200",
            "msg": "Award updated successfully."
        } 
        
def deleteAward(request):
        id = request.GET.get("id")
    
        award = Awards.objects.filter(id=id).first()
    
        if not award:
            return {
                "code": "404",
                "msg": "Award not found."
            }
    
        award.delete()
    
        return {
            "code": "200",
            "msg": "Award deleted successfully."
        }
        
        ##--------------------------------------Images ------------------------------
def addImage(request):
    data = request.data

    doctor_id = data.get("doctor_id")
    image = request.FILES.get("image")

    if not doctor_id or not image:
        return {
            "code": "400",
            "msg": "doctor_id and image are required."
        }

    doctor = Doctor.objects.filter(id=doctor_id).first()

    if not doctor:
        return {
            "code": "404",
            "msg": "Doctor not found."
        }

    if doctor.images.count() >= 5:
        return {
            "code": "400",
            "msg": "Maximum 5 images are allowed for a doctor."
        }

    Images.objects.create(
        doctor=doctor,
        image=image
    )

    return {
        "code": "200",
        "msg": "Image added successfully."
    }

def getImageList(request):
    doctor_id = request.GET.get("doctor_id")

    if not doctor_id:
        return {
            "code": "400",
            "msg": "doctor_id is required."
        }

    images = Images.objects.filter(doctor_id=doctor_id)

    serializer = ImageSerializer(
        images,
        many=True,
        context={"request": request}
    )

    return {
        "code": "200",
        "list": serializer.data
    }
    
def updateImage(request):
    data = request.data

    id = data.get("id")
    image = request.FILES.get("image")

    image_obj = Images.objects.filter(id=id).first()

    if not image_obj:
        return {
            "code": "404",
            "msg": "Image not found."
        }

    if image:
        image_obj.image = image
        image_obj.save()

    return {
        "code": "200",
        "msg": "Image updated successfully."
    }

def deleteImage(request):
    id = request.GET.get("id")

    image = Images.objects.filter(id=id).first()

    if not image:
        return {
            "code": "404",
            "msg": "Image not found."
        }

    image.delete()

    return {
        "code": "200",
        "msg": "Image deleted successfully."
    }