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

class Doctor_details(APIView):
    def get(self,request):
        detail=doctor_models.Doctordetails.objects.all()
        if not detail:
             return Response({'success':'false',
                                'error_msg':'Not found',
                                'errors':'',
                                'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)
        return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':{'resule':serializers.doctor_serializer(detail[0]).data},
                            },status=status.HTTP_200_OK)
    def post(self,request):
        f1=serializers.doctor_models(data=request.POST)
        if f1.is_valid():
            return Response({'success':'true',
                                        'error_msg':'',
                                        'errors':{},
                                        'response':{},
                                        },status.HTTP_202_ACCEPTED)    
                
        else:
            return Response({'success':'false',
                                'error_msg':'invalid_inputs',
                                'errors':dict(f1.errors),
                                'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)

    def put(self,request):
        try:
            user=doctor_models.Doctordetails.objects.filter(email=request.POST['email'])
            f1=serializers.doctor_serializer(data=request.POST,instance=user)
            if f1.is_valid():
                return Response({'success':'true',
                                            'error_msg':'',
                                            'errors':{},
                                            'response':{},
                                            },status.HTTP_202_ACCEPTED)    

            else:
                return Response({'success':'false',
                                        'error_msg':'invalid_inputs',
                                        'errors':{},
                                        'response':{},
                                        },status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'success':'false',
                                'error_msg':str(e),
                                'errors':'',
                                'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)



class Appointment(APIView):
    def get(self,request):
        appoint=doctor_models.DoctorAppoinment.objects.all()
        if not appoint:
             return Response({'success':'false',
                                'error_msg':'Not found',
                                'errors':'',
                                'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)
        return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':{'result':serializers.Appointment_serializer(appoint[0]).data},
                            },status=status.HTTP_200_OK)



    def post(self,request):
        appoint=doctor_models.DoctorAppoinment()
        appoint.hospital_name=request.POST['hospital_name']
        appoint.patient_problem=request.POST['patient_problem']
        appoint.start_appointment=request.POST['start_appointment']
        appoint.end_appointment=request.POST['end_appointment']
        appoint.repeated_patient=request.POST['repeated_patient']
        appoint.first_name=request.POST['first_name']
        appoint.last_name=request.POST['last_name']
        appoint.date_of_birth=request.POST['date_of_birth']
        appoint.gender=request.POST['gender']
        appoint.email=request.POST['email']
        appoint.country_code=request.POST['country_code']
        appoint.phone_number=request.POST['phone_number']
        appoint.country=request.POST['country']
        appoint.city=request.POST['city']
        appoint.state=request.POST['state']
        appoint.zip_code=request.POST['zip_code']
        appoint.address_line_1=request.POST['address_line_1']
        appoint.address_line_2=request.POST['address_line_2']
        appoint.save()
        return Response({'success':'true',
                         'error_msg':'',
                         'errors':{},
                         'response':{},
                        },status.HTTP_202_ACCEPTED)  


