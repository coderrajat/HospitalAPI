from django.db import models

class Patientbills(models.Model):
    patient_problem=models.TextField(default='')
    hospital_name=models.CharField(max_length=100,default='')
    patient_first_name=models.CharField(max_length=100)
    Patient_last_name=models.CharField(max_length=100)
    services_taken=models.CharField(max_length=100)
    total_time=models.TextField(default='')
    amount=models.CharField(max_length=100,default='0')
    service_charge=models.CharField(max_length=100,default='0')
    additional_charges=models.CharField(max_length=100,default='0')
    discount=models.CharField(max_length=100,default='0')
    tax=models.CharField(max_length=100,default='0')
    total=models.CharField(max_length=100,default='0')
    invoice_id= models.TextField(unique=True)
    invoice_date=models.DateTimeField(auto_now_add=True)
