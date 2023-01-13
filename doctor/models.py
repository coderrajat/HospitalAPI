from django.db import models


class Doctordetails(models.Model):
    docter_start_time=models.DateTimeField(verbose_name='start_appointment', auto_now=True)
    docter_close_time=models.DateTimeField(verbose_name='start_appointment', auto_now=True)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    email=models.EmailField(verbose_name="email", max_length=60)
    country_code=models.CharField(max_length=10)
    phone_number=models.CharField(max_length=15)
    country=models.CharField(max_length=100,default='')
    city=models.CharField(max_length=100,default='')
    state=models.CharField(max_length=100,default='')
    zip_code=models.CharField(max_length=100,default='')
    address_line_1=models.CharField(max_length=200,default='')
    address_line_2=models.CharField(max_length=200,default='')

class DoctorAppoinment(models.Model):
    doctor=models.ForeignKey(Doctordetails,on_delete=models.DO_NOTHING,related_name='appointment')
    hospital_name=models.CharField(max_length=100,default='')
    patient_problem=models.TextField(default='')
    start_appointment=models.DateTimeField(verbose_name='start_appointment', auto_now=True)
    end_appointment=models.DateTimeField(verbose_name='start_appointment', auto_now=True)
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


