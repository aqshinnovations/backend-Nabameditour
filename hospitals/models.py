from django.db import models


class Hospital(models.Model):
    name_en = models.CharField(max_length=255,null=True,blank=True)
    name_ar = models.CharField(max_length=255, blank=True, null=True)

    description_en = models.TextField(blank=True, null=True)
    description_ar = models.TextField(blank=True, null=True)
    
    location_en = models.CharField(max_length=255, null=True, blank=True)
    location_ar = models.CharField(max_length=255, null=True, blank=True)
    
    image = models.ImageField(upload_to="hospitals/", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["-created_at"]
        
    def __str__(self):
        return self.name_en
    
    @staticmethod
    def getByName(name_en):
        if Hospital.objects.filter(name_en=name_en).exists():
            return Hospital.objects.get(name_en=name_en)
        return None

    @staticmethod
    def getByEmail(email):
        email = str(email).lower()
        print("getByEmail >> ", email)
        if Hospital.objects.filter(email=email).exists():
            return Hospital.objects.get(email=email)
        return None
    
    
class Specialization(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name="specializations")
   
    name_en = models.CharField(max_length=255,null=True, blank=True)
    name_ar = models.CharField(max_length=255, blank=True, null=True)
    


    def __str__(self):
        return self.name_en
    
class Facilities(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name="Facilities")
   
    name_en = models.CharField(max_length=255,null=True, blank=True)
    name_ar = models.CharField(max_length=255, blank=True, null=True)
    


    def __str__(self):
        return self.name_en
    
class Doctor(models.Model):
    hospital = models.ForeignKey(
        Hospital,
        on_delete=models.CASCADE,
        related_name="doctors"
    )

    name_en = models.CharField(max_length=255)
    name_ar = models.CharField(max_length=255, blank=True, null=True)

    specialist_en = models.CharField(max_length=255)
    specialist_ar = models.CharField(max_length=255, blank=True, null=True)

    image = models.ImageField(upload_to="doctors/", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name_en"]

    def __str__(self):
        return self.name_en


class Procedure(models.Model):
    hospital = models.ForeignKey(
        Hospital,
        on_delete=models.CASCADE,
        related_name="procedures"
    )

    name_en = models.CharField(max_length=255)
    name_ar = models.CharField(max_length=255, blank=True, null=True)

    description_en = models.TextField(blank=True, null=True)
    description_ar = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    image = models.ImageField(upload_to="procedures/", blank=True, null=True)
    

    class Meta:
        ordering = ["name_en"]

    def __str__(self):
        return self.name_en
