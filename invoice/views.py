from distutils.log import error
from . import models as doctor_models
from invoice import models as invoice_models
from django.db.models import Q,F
from . import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.serializers import serialize
from django.http import HttpResponse

class invoice(APIView):
    def get(self,request,id):
        invo=invoice_models.Patientbills.objects.filter(id=id)
        if not invo:
            return Response({'success':'false',
                                'error_msg':'Not found',
                                'errors':'',
                                'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)

        invo=invo[0]
        return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':{'resule':serializers.invoiceserializer(invo).data},
                            },status=status.HTTP_200_OK)