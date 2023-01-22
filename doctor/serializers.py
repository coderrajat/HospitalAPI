from typing import Literal
from rest_framework import serializers
from . import models as doctor_models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from invoice import models as invoice_models



# class Appointment_serializer(serializers.ModelSerializer):
#     class Meta():
#         model=doctor_models.DoctorAppoinment
#         exclude=('doctor','hospital_name')
        

# class doctor_serializer(serializers.ModelSerializer):
#     class Meta():
#         model=doctor_models.Doctordetails
#         fields=('__all__')
