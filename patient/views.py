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
from accounts.tools import code, decode, codetoken, decodetoken, get_user
import datetime,pytz


def is_authenticate(*Dargs,**Dkwargs):
    def inner(fun):
        def wrapper(*args,**kwargs):
            if 'HTTP_AUTHORIZATION'in args[1].META :
                try:
                    data=decodetoken(args[1].META['HTTP_AUTHORIZATION'])
                    time=datetime.datetime.strptime(data[2].split('.')[0],'%Y-%m-%d %H:%M:%S')
                except Exception as e:
                    return Response({'success':'false','error_msg':'invalid token','errors':{},'response':{}},status=status.HTTP_401_UNAUTHORIZED)
                    
                print(data,time)
                if len(data)==4 and time>datetime.datetime.now():
                    uzr= get_user(*data)
                    print(uzr)
                    if uzr!=[]:
                        if uzr.is_user_blocked :
                            return Response({'success':'false',
                                            'error_msg':'USER BLOCKED',
                                            'errors':{},
                                            'response':{}},status=status.HTTP_401_UNAUTHORIZED)
                        if uzr.is_active==False:
                            return Response({'success':'false',
                                            'error_msg':'USER DEACTIVATED',
                                            'errors':{},
                                            'response':{}},status=status.HTTP_401_UNAUTHORIZED)
                        if uzr.is_verified==False:
                            return Response({'success':'false',
                                            'error_msg':'USER NOT VERIFIED',
                                            'errors':{},
                                            'response':{}},status=status.HTTP_401_UNAUTHORIZED)
                        return fun(*args,**kwargs)

                    else:
                        return Response({'success':'false',
                                        'error_msg':'USER NOT LOGGEDIN',
                                        'errors':{},
                                        'response':{}},status=status.HTTP_401_UNAUTHORIZED)
                return Response({'success':'false',
                                'error_msg':'token expire',
                                'errors':{},
                                'response':{}},status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'success':'false',
                                'error_msg':'no HTTP_AUTHORIZATION ',
                                'errors':{},
                                'response':{}},status=status.HTTP_401_UNAUTHORIZED)
            # return fun(*args,**kwargs)
        return wrapper
    return inner


class Patientdetails(APIView):
    def get(self,request):
        f1=serializers.booking_fields()
        return Response({**f1.data,
                        'token':'required'},status=status.HTTP_202_ACCEPTED)
    
    @is_authenticate()
    def post(self,request):
        data=decodetoken(request.META['HTTP_AUTHORIZATION'])
        requstuser=get_user(*data)
        appoint=doctor_models.Patient()
        appoint.user=requstuser
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