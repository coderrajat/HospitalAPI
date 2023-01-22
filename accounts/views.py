from . import models
from . import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
import random
from django.db.models import Q
from doctor import models as doctor_models
import pytz,datetime
import secrets
import bcrypt
from google.auth.transport import requests
from google.oauth2 import id_token
import jwt

from .tools import  code, decode, codetoken, decodetoken, get_user, get_base64_to_img



def login_required(*ag,**kg):
    def inner(func):
        def wrapper(*args,**kwargs):
            if 'HTTP_AUTHORIZATION'in args[1].META :
                try:
                    data=decodetoken(args[1].META['HTTP_AUTHORIZATION'])
                    time=datetime.datetime.strptime(data[2].split('.')[0],'%Y-%m-%d %H:%M:%S')
                except:
                    return Response({'success':'false','error_msg':'invalid token','errors':{},'response':{}},status=status.HTTP_401_UNAUTHORIZED)
                if len(data)==4 and time>datetime.datetime.now():
                    uzr= get_user(*data)
                    if uzr!=[]:
                        if uzr.token.token=='':
                            return Response({'success':'false','error_msg':'USER NOT LOGGEDIN','errors':{},'response':{}},status=status.HTTP_401_UNAUTHORIZED)
                        return func(*args,**kwargs)
                    else:
                        return Response({'success':'false','error_msg':'USER NOT LOGGEDIN','errors':{},'response':{}},status=status.HTTP_401_UNAUTHORIZED)
                return Response({'success':'false','error_msg':'token expire','errors':{},'response':{}},status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'success':'false','error_msg':'no HTTP_AUTHORIZATION ','errors':{},'response':{}},status=status.HTTP_401_UNAUTHORIZED)
            return func(*args,**kwargs)
        return wrapper
    return inner


def login_user(userid,token=''):
    token=codetoken(userid,type='user',token=token)
    return token

class User_SignUp(APIView):
    """This class use to Create the user account or it takes the Signup details """
    def get(self,request):
        f0=serializers.Password()
        f1=serializers.Create_User_form()

        return Response({**f1.data,**f0.data
                            },status=status.HTTP_202_ACCEPTED)

    def post(self, request):
        f1=serializers.Create_User_form(data=request.POST)
        if 'ts_agree' not in request.POST: #this code write becouse In frontend are used term and condition checkbox
            return Response({'success':'false',
                            'error_msg':'Please terms and usage not checked',
                            'errors':{'ts_agree':'is not checked'},
                            'response':{},
                            },status=status.HTTP_400_BAD_REQUEST)
        if f1.is_valid():
            if request.POST['ts_agree']!='true':
                return Response({'success':'false',
                                'error_msg':'Please terms and usage not checked',
                                'errors':{'ts_agree':'is not checked'},
                                'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)
            ref_uzr=''
            if 'referral_code' in request.POST and request.POST['referral_code']!='':   #This feature are used most of the website for marketing by the user side
                ref_uzr=list(models.User.objects.filter(referral_code=request.POST['referral_code']))
                if ref_uzr==[]:
                    return Response({'success':'false',
                                        'error_msg':'ref_uzr is invalid',
                                        'errors':{},
                                        'response':{},
                                        },status=status.HTTP_400_BAD_REQUEST)
                ref_uzr=ref_uzr[0]
            check_list = list(models.User.objects.filter((Q(country_code=request.POST['country_code'])&Q(phone_number=request.POST['phone_number']))|
                                                                        Q(email=request.POST['email'])))
            del_acc=[]
            if check_list != []:
                for i in check_list:
                    if i.country_code==request.POST['country_code'] and i.phone_number==request.POST['phone_number'] and i.is_verified==True:
                        return Response({'success':'false',
                                        'error_msg':'This phone number already exists',
                                        'errors':{},
                                        'response':{},
                                        },status=status.HTTP_400_BAD_REQUEST)
                    elif i.email==request.POST['email'] and i.is_verified==True:
                        return Response({'success':'false',
                                        'error_msg':'This email already exists',
                                        'errors':{},
                                        'response':{},
                                        },status=status.HTTP_400_BAD_REQUEST)
                    else:
                        del_acc.append(i)
            if del_acc!=[]:
                for i in del_acc:
                    i.delete()
            sec=''
            val=[1,2,3,4,5,6,7,8,9]
            otp_p=str(random.choice(val))
            for i in range(5):
                otp_p+=str(random.choice(val))
                sec+=secrets.choice(secrets.choice([chr(ii) for ii in range(45,123)]))

            try:
                uzr=models.User()
                uzr.first_name=request.POST['first_name']
                uzr.last_name=request.POST['last_name']
                uzr.user_type='User'
                uzr.country_code=request.POST['country_code']
                uzr.phone_number=request.POST['phone_number']
                uzr.email=request.POST['email']
                uzr.address_line_1=request.POST['address1']
                uzr.address_line_2=request.POST['address2']
                uzr.city=request.POST['city']
                uzr.state=request.POST['state']
                uzr.country=request.POST['country']
                if  'profile_pic' in request.FILES:
                    uzr.profile_pic=request.FILES['profile_pic']
                uzr.zip_code=request.POST['zip_code']
                uzr.username=request.POST['email']
                uzr.otp=otp_p
                uzr.save()

                uzr.referal_number=hex(uzr.id)
                password=request.POST['password'].encode('utf-8')
                uzr.password=bcrypt.hashpw(password,bcrypt.gensalt())  #here this haspw conver the alpha numecic password in to hash values
            
                uzr.password=uzr.password.decode("utf-8")
                uzr.is_active=True
                uzr.is_verified=True
                uzr.save()
                uzr_token=models.User_token(user=uzr,token=sec)
                uzr_token.save()
                return Response({'success':'true',
                                'error_msg':'',
                                'errors':{},
                                'response':{},
                                },status=status.HTTP_202_ACCEPTED)
            except Exception as e:
                return Response({'success':'false',
                                'error_msg':"Something Bad happened",
                                'errors':{},
                                'response':str(e),
                                },status=status.HTTP_400_BAD_REQUEST)

           

        else:
            return Response({'success':'false',
                                'error_msg':'requried fields',
                                'errors':{**dict(f1.errors)},
                                'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)


class User_Login(APIView):
    def get(self,request):
        f1=serializers.Login()
        return Response(f1.data,status=status.HTTP_202_ACCEPTED)

    def post(self,request):
        f1=serializers.Login(data=request.data)
        if (f1.is_valid()):
            user=list(models.User.objects.filter(email=request.POST['email']))
            if user!=[]:
                user=user[0]
            else:
                return Response({'success':'false',
                                    'error_msg':'User does not exist',
                                    'errors':'Invalid email',
                                    'response':{},

                                },status=status.HTTP_400_BAD_REQUEST)
            if (user.is_active==False):
                return Response({'success':'false',
                                    'error_msg':'Your account is not active',
                                    'errors':'',
                                    'response':{},

                                },status=status.HTTP_400_BAD_REQUEST)
            password=str(request.POST['password']).encode('utf-8')
            hash_pass=user.password.encode('utf-8')
            if bcrypt.checkpw(password,hash_pass):
                sec=''
                for i in range(10):
                    sec+=secrets.choice(secrets.choice([chr(ii) for ii in range(45,123)]))

                user.token.token=sec
                print(sec,'sec')
                user.last_login=datetime.datetime.now()
                user.token.save()
                re=login_user(user.id,token=sec)
                return Response({'success':'true',
                                    'error_msg':'',
                                    'errors':{},
                                    'response':{'user':[serializers.User_login_forms(user).data],},
                                    'token':re,
                                    # 'auth':{'sessionid':request.session.session_key,
                                    #         'csrftoken':request.META['CSRF_COOKIE']


                                },status=status.HTTP_202_ACCEPTED)

            return Response({'success':'false',
                                'error_msg':'user_not_authenticated',
                                'response':{},
                                'errors':dict(f1.errors),

                                },status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'success':'false',
                                'error_msg':'Invalid username and password',
                                'errors':dict(f1.errors),
                                'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)



class Doctor_SignUp(APIView):
    """This class use to Create the user account or it takes the Signup details """
    def get(self,request):
        f0=serializers.Password()
        f1=serializers.Create_User_form()

        return Response({**f1.data,**f0.data
                            },status=status.HTTP_202_ACCEPTED)

    def post(self, request):
        f1=serializers.Create_Doctor_form(data=request.POST)
        if 'ts_agree' not in request.POST: #this code write becouse In frontend are used term and condition checkbox
            return Response({'success':'false',
                            'error_msg':'Please terms and usage not checked',
                            'errors':{'ts_agree':'is not checked'},
                            'response':{},
                            },status=status.HTTP_400_BAD_REQUEST)
        if f1.is_valid():
            if request.POST['ts_agree']!='true':
                return Response({'success':'false',
                                'error_msg':'Please terms and usage not checked',
                                'errors':{'ts_agree':'is not checked'},
                                'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)
            ref_uzr=''
            if 'referral_code' in request.POST and request.POST['referral_code']!='':   #This feature are used most of the website for marketing by the user side
                ref_uzr=list(models.Doctor.objects.filter(referral_code=request.POST['referral_code']))
                if ref_uzr==[]:
                    return Response({'success':'false',
                                        'error_msg':'ref_uzr is invalid',
                                        'errors':{},
                                        'response':{},
                                        },status=status.HTTP_400_BAD_REQUEST)
                ref_uzr=ref_uzr[0]
            check_list = list(models.Doctor.objects.filter((Q(country_code=request.POST['country_code'])&Q(phone_number=request.POST['phone_number']))|
                                                                        Q(email=request.POST['email'])))
            del_acc=[]
            if check_list != []:
                for i in check_list:
                    if i.country_code==request.POST['country_code'] and i.phone_number==request.POST['phone_number'] and i.is_verified==True:
                        return Response({'success':'false',
                                        'error_msg':'This phone number already exists',
                                        'errors':{},
                                        'response':{},
                                        },status=status.HTTP_400_BAD_REQUEST)
                    elif i.email==request.POST['email'] and i.is_verified==True:
                        return Response({'success':'false',
                                        'error_msg':'This email already exists',
                                        'errors':{},
                                        'response':{},
                                        },status=status.HTTP_400_BAD_REQUEST)
                    else:
                        del_acc.append(i)
            if del_acc!=[]:
                for i in del_acc:
                    i.delete()
            sec=''
            val=[1,2,3,4,5,6,7,8,9]
            otp_p=str(random.choice(val))
            for i in range(5):
                otp_p+=str(random.choice(val))
                sec+=secrets.choice(secrets.choice([chr(ii) for ii in range(45,123)]))

            try:
                uzr=models.User()
                uzr.first_name=request.POST['first_name']
                uzr.last_name=request.POST['last_name']
                uzr.user_type='User'
                uzr.country_code=request.POST['country_code']
                uzr.phone_number=request.POST['phone_number']
                uzr.email=request.POST['email']
                uzr.address_line_1=request.POST['address1']
                uzr.address_line_2=request.POST['address2']
                uzr.city=request.POST['city']
                uzr.state=request.POST['state']
                uzr.country=request.POST['country']
                if  'profile_pic' in request.FILES:
                    uzr.profile_pic=request.FILES['profile_pic']
                uzr.zip_code=request.POST['zip_code']
                uzr.username=request.POST['email']
                uzr.otp=otp_p
                uzr.save()

                uzr.referal_number=hex(uzr.id)
                password=request.POST['password'].encode('utf-8')
                uzr.password=bcrypt.hashpw(password,bcrypt.gensalt())  #here this haspw conver the alpha numecic password in to hash values
            
                uzr.password=uzr.password.decode("utf-8")
                uzr.is_active=True
                uzr.is_verified=True
                uzr.save()
                uzr_token=models.User_token(user=uzr,token=sec)
                uzr_token.save()
                return Response({'success':'true',
                                'error_msg':'',
                                'errors':{},
                                'response':{},
                                },status=status.HTTP_202_ACCEPTED)
            except Exception as e:
                return Response({'success':'false',
                                'error_msg':"Something Bad happened",
                                'errors':{},
                                'response':str(e),
                                },status=status.HTTP_400_BAD_REQUEST)

           

        else:
            return Response({'success':'false',
                                'error_msg':'requried fields',
                                'errors':{**dict(f1.errors)},
                                'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)


class Doctor_Login(APIView):
    def get(self,request):
        f1=serializers.Login()
        return Response(f1.data,status=status.HTTP_202_ACCEPTED)

    def post(self,request):
        f1=serializers.Login(data=request.data)
        if (f1.is_valid()):
            user=list(models.User.objects.filter(email=request.POST['email']))
            if user!=[]:
                user=user[0]
            else:
                return Response({'success':'false',
                                    'error_msg':'User does not exist',
                                    'errors':'Invalid email',
                                    'response':{},

                                },status=status.HTTP_400_BAD_REQUEST)
            if (user.is_active==False):
                return Response({'success':'false',
                                    'error_msg':'Your account is not active',
                                    'errors':'',
                                    'response':{},

                                },status=status.HTTP_400_BAD_REQUEST)
            password=str(request.POST['password']).encode('utf-8')
            hash_pass=user.password.encode('utf-8')
            if bcrypt.checkpw(password,hash_pass):
                sec=''
                for i in range(10):
                    sec+=secrets.choice(secrets.choice([chr(ii) for ii in range(45,123)]))

                user.token.token=sec
                print(sec,'sec')
                user.last_login=datetime.datetime.now()
                user.token.save()
                re=login_user(user.id,token=sec)
                return Response({'success':'true',
                                    'error_msg':'',
                                    'errors':{},
                                    'response':{'user':[serializers.User_login_forms(user).data],},
                                    'token':re,
                                    # 'auth':{'sessionid':request.session.session_key,
                                    #         'csrftoken':request.META['CSRF_COOKIE']


                                },status=status.HTTP_202_ACCEPTED)

            return Response({'success':'false',
                                'error_msg':'user_not_authenticated',
                                'response':{},
                                'errors':dict(f1.errors),

                                },status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'success':'false',
                                'error_msg':'Invalid username and password',
                                'errors':dict(f1.errors),
                                'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)