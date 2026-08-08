
from .models import Patients
from django.utils import timezone
from .serializer import PatientsSerializer
from django.http import FileResponse, Http404


def savePatients(request):
    adminUser = request.user
    data = request.data

    name = data.get("name", None)
    email = data.get("email", None)
    mobile = data.get("mobile", None)
    aboutHealth = data.get("aboutHealth", None)
    report = request.FILES.get("report") 

    if not name or not mobile:
        return {
            "code": "400",
            "msg": "Bad request. Please ensure all required fields are provided",
        }

    patientsDetails = Patients()
    patientsDetails.name = name
    patientsDetails.email = email
    patientsDetails.mobile = mobile
    patientsDetails.report = report
    patientsDetails.aboutHealth = aboutHealth 

    patientsDetails.save()

    data = {
        "code": "200",
        "msg": "Patients Details Saved successfully!",
    }
    return data


def listPatients(request):
    patientsList = Patients.objects.all()
    patientsSerializer = PatientsSerializer(patientsList, many=True, context={"request": request})

    return {"code": "200", "list": patientsSerializer.data}



def deletePatients(request):
    data = request.GET
    id = data.get("id", None)

    if not id:
        return {
            "code": "400",
            "msg": "Bad request. Please ensure all required fields are provided.",
        }

    patients = Patients.objects.filter(id=id).first()
    if not patients:
        return {"code": "401", "msg": "No record found with the provided ID."}

    patients.delete()
    return {"code": "200", "msg": "patients Data deleted successfully!"}

def downloadPatientReport(request):
    data = request.GET
    patient_id = data.get("id", None)

    if not patient_id:
        return {
            "code": "400",
            "msg": "Bad request. Please provide patient ID."
        }

    patient = Patients.objects.filter(id=patient_id).first()
    if not patient or not patient.report:
        return {
            "code": "404",
            "msg": "Report not found for the provided ID."
        }

    try:
        response = FileResponse(open(patient.report.path, 'rb'), as_attachment=True, filename=patient.report.name.split('/')[-1])
        return response
    except Exception as e:
        return {
            "code": "500",
            "msg": "Failed to download report.Please try again"
        }