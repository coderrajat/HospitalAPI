from typing import Literal
from rest_framework import serializers
from doctor import models as doctor_models
from invoice import models as invoice_models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _



class invoiceserializer(serializers.ModelSerializer):
    class Meta():
        model=invoice_models.Patientbills
        fields=('__all__')
        
