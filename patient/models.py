from django.db import models
from accounts.models import Admin,User,Doctor




class Patient(models.Model):
    admin=models.ForeignKey(Admin,on_delete=models.DO_NOTHING,related_name='admin_can_view',default='',null=True)
    user=models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name='user_can_view',default='',null=True)
    doctor=models.ForeignKey(Doctor,on_delete=models.DO_NOTHING,related_name='doctor_can_view',default='',null=True)

    hospital_name=models.CharField(max_length=100,default='')
    patient_problem=models.TextField(default='')
    start_appointment=models.DateTimeField(verbose_name='start_appointment', auto_now=True)
    end_appointment=models.DateTimeField(verbose_name='end_appointment', auto_now=True)
    repeated_patient=models.BooleanField(default=False)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    date_of_birth=models.CharField(max_length=100)
    gender=models.CharField(max_length=100)
    email=models.EmailField(verbose_name="email", max_length=60)
    country_code=models.CharField(max_length=10)
    phone_number=models.CharField(max_length=15)
    country=models.CharField(max_length=100,default='')
    city=models.CharField(max_length=100,default='')
    state=models.CharField(max_length=100,default='')
    zip_code=models.CharField(max_length=100,default='')
    address_line_1=models.CharField(max_length=200,default='')
    address_line_2=models.CharField(max_length=200,default='')

