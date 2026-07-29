from .models import Category,Doctor
from .serializer import CategoriesSerializer,DoctorsSerializer,DoctorsDetailSerializer

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
    doctors.category = category      # <-- Add this line
     
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




