from django.db import models
from django.db.models.deletion import CASCADE
from authorize.models import CustomUser
from django.urls import reverse

class patient(models.Model):
    full_name = models.CharField(max_length=100)
    appointment = models.DateField(null=True, blank=True)
    doctor = models.ForeignKey(CustomUser, on_delete=models.RESTRICT)

    def __str__(self):
        return self.full_name
    
    def get_absolute_url(self):
        return reverse("patient", args=[str(self.id)])
    
    
class cholesterol(models.Model):
    total_cholesterol = models.CharField(max_length=50, null=False, blank=False)
    patient = models.ForeignKey(patient, on_delete=models.RESTRICT, blank=False)
    

    def __str__(self):
        return self.total_cholesterol

class LDL(models.Model):
    ldl = models.CharField(max_length=50, blank=False)
    patient = models.ForeignKey(patient, on_delete=models.RESTRICT, blank=False)
    

    def __str__(self):
        return self.ldl

class HDL(models.Model):
    hdl = models.CharField(max_length=50, blank=False)
    patient = models.ForeignKey(patient, on_delete=models.RESTRICT, blank=False)
    

    def __str__(self):
        return self.hdl

class TG(models.Model):
    tg = models.CharField(max_length=50, blank=False)
    patient = models.ForeignKey(patient, on_delete=models.RESTRICT, blank=False)
    

    def __str__(self):
        return self.tg

class log(models.Model):
    date = models.DateField(null=True, blank=True)
    ldl = models.ForeignKey(LDL, on_delete=models.RESTRICT, null=True, blank=True)
    tc = models.ForeignKey(cholesterol, blank=True, null=True, on_delete=models.CASCADE)
    hdl = models.ForeignKey(HDL, null=True, on_delete=CASCADE)
    tg = models.ForeignKey(TG, null=True, on_delete=CASCADE)
    patient = models.ForeignKey(patient, on_delete=models.RESTRICT)

    def __str__(self):
        return str(self.date)
    
    def get_absolute_url(self):
        return reverse("log-detail", args=[str(self.id)])
    