from django.db import models


class Patients(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)   
    email = models.EmailField(max_length=100, null=True, blank=True)   
    mobile = models.CharField(max_length=15, null=False, blank=False)  
    report = models.FileField(upload_to="patients/reports/", null=True, blank=True)  
    aboutHealth = models.TextField(max_length=200, null=True, blank=True)  
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} - {self.name} - {self.mobile}"

    class Meta:
        db_table = "patients"


