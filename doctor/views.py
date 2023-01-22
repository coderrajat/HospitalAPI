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
                    #print('\ndata=',data)
                    time=datetime.datetime.strptime(data[2].split('.')[0],'%Y-%m-%d %H:%M:%S')
                except Exception as e:
                    return Response({'success':'false','error_msg':'invalid token','errors':{},'response':{}},status=status.HTTP_401_UNAUTHORIZED)

                if len(data)==4 and time>datetime.datetime.now():
                    uzr= get_user(*data)
                    if uzr!=[]:
                        if uzr.is_user_blocked :
                            return Response({'success':'false','error_msg':'USER BLOCKED','errors':{},'response':{}},status=status.HTTP_401_UNAUTHORIZED)
                        if uzr.is_active==False:
                            return Response({'success':'false','error_msg':'USER DEACTIVATED','errors':{},'response':{}},status=status.HTTP_401_UNAUTHORIZED)
                        if uzr.is_verified==False:
                            return Response({'success':'false','error_msg':'USER NOT VERIFIED','errors':{},'response':{}},status=status.HTTP_401_UNAUTHORIZED)
                        return fun(*args,**kwargs)

                    else:
                        return Response({'success':'false','error_msg':'USER NOT LOGGEDIN','errors':{},'response':{}},status=status.HTTP_401_UNAUTHORIZED)
                return Response({'success':'false','error_msg':'token expire','errors':{},'response':{}},status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'success':'false','error_msg':'no HTTP_AUTHORIZATION ','errors':{},'response':{}},status=status.HTTP_401_UNAUTHORIZED)
            # return fun(*args,**kwargs)
        return wrapper
    return inner





# class Doctor_details(APIView):
#     def get(self,request):
#         detail=doctor_models.Doctordetails.objects.all()
#         if not detail:
#              return Response({'success':'false',
#                                 'error_msg':'Not found',
#                                 'errors':'',
#                                 'response':{},
#                                 },status=status.HTTP_400_BAD_REQUEST)
#         return Response({'success':'true',
#                             'error_msg':'',
#                             'errors':{},
#                             'response':{'resule':serializers.doctor_serializer(detail[0]).data},
#                             },status=status.HTTP_200_OK)
#     def post(self,request):
#         f1=serializers.doctor_models(data=request.POST)
#         if f1.is_valid():
#             return Response({'success':'true',
#                                         'error_msg':'',
#                                         'errors':{},
#                                         'response':{},
#                                         },status.HTTP_202_ACCEPTED)    
                
#         else:
#             return Response({'success':'false',
#                                 'error_msg':'invalid_inputs',
#                                 'errors':dict(f1.errors),
#                                 'response':{},
#                                 },status=status.HTTP_400_BAD_REQUEST)

#     def put(self,request):
#         try:
#             user=doctor_models.Doctordetails.objects.filter(email=request.POST['email'])
#             f1=serializers.doctor_serializer(data=request.POST,instance=user)
#             if f1.is_valid():
#                 return Response({'success':'true',
#                                             'error_msg':'',
#                                             'errors':{},
#                                             'response':{},
#                                             },status.HTTP_202_ACCEPTED)    

#             else:
#                 return Response({'success':'false',
#                                         'error_msg':'invalid_inputs',
#                                         'errors':{},
#                                         'response':{},
#                                         },status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             return Response({'success':'false',
#                                 'error_msg':str(e),
#                                 'errors':'',
#                                 'response':{},
#                                 },status=status.HTTP_400_BAD_REQUEST)






