from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

"""This account section convers the account information like Patient(user) SignUp details
 and Doctor Sign in Details and Administrator Sign in details"""


class UserAccountManager(BaseUserManager):
    """Her we managed the all accounts from the django admin panel So before create account we need his info """
    def create_user(self, email,first_name,last_name,country_code,phone_number, password=None):
        if not email:
            raise 'User must have an Email'

        user =self.model(email=self.normalize_email(email),
                        first_name=first_name,
                        last_name=last_name,
                        country_code=country_code,
                        phone_number=phone_number)
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superadmin(self, email, first_name,last_name,country_code,phone_number,password=None):
        user = self.create_user(
			email=self.normalize_email(email),
			password=password,
            first_name=first_name,
            last_name=last_name,
			country_code=country_code,
			phone_number=phone_number,
		)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email=models.EmailField(verbose_name="email", max_length=60)
    username=models.CharField(verbose_name="nic name",max_length=30,default='')
    date_joined=models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login=models.DateTimeField(verbose_name='last login', auto_now=True)
    is_active=models.BooleanField(default=True)
    is_admin=models.BooleanField(default=False) #it is define the type of status of user
    is_staff=models.BooleanField(default=False) #it is define the type of status of user
    is_superuser=models.BooleanField(default=False) #it is define the type of status of user
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    user_type= models.CharField(max_length=12,default='user')
    address_line_1=models.CharField(max_length=200,default='')
    address_line_2=models.CharField(max_length=200,default='')
    profile_pic=models.ImageField(upload_to='admin/image/profile_image',default='deafult_profile_pic.jpeg')
    is_verified=models.BooleanField(default=False)
    referal_number=models.CharField(max_length=200,default='') #this is alpha numeric to use send referal to other user
    otp=models.CharField(max_length=200,default='')
    country_code=models.CharField(max_length=10)
    phone_number=models.CharField(max_length=15)
    country=models.CharField(max_length=100,default='')
    city=models.CharField(max_length=100,default='')
    state=models.CharField(max_length=100,default='')
    zip_code=models.CharField(max_length=100,default='')
    is_user_blocked=models.BooleanField(default=False)
    timezone=models.TextField(default="UTC")
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['email', 'first_name','last_name','country_code','phone_number']
    objects=UserAccountManager()
    def has_perm(self, perm, obj=None):
        return self.is_admin
    def has_module_perms(self, app_label):
        return True

class DoctorAccountManager(BaseUserManager):
    """Her we managed the all accounts from the django admin panel So before create account we need his info """
    def create_user(self, email,first_name,last_name,country_code,phone_number, password=None):
        if not email:
            raise 'User must have an Email'

        user =self.model(email=self.normalize_email(email),
                        first_name=first_name,
                        last_name=last_name,
                        country_code=country_code,
                        phone_number=phone_number)
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superadmin(self, email, first_name,last_name,country_code,phone_number,password=None):
        user = self.create_user(
			email=self.normalize_email(email),
			password=password,
            first_name=first_name,
            last_name=last_name,
			country_code=country_code,
			phone_number=phone_number,
		)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
class Doctor(AbstractBaseUser):
    email=models.EmailField(verbose_name="email", max_length=60)
    username=models.CharField(verbose_name="nic name",max_length=30,default='')
    date_joined=models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login=models.DateTimeField(verbose_name='last login', auto_now=True)
    is_active=models.BooleanField(default=True) 
    is_admin=models.BooleanField(default=False) #it is define the type of status of user
    is_staff=models.BooleanField(default=False) #it is define the type of status of user
    is_superuser=models.BooleanField(default=False) #it is define the type of status of user
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    user_type= models.CharField(max_length=12,default='Docter')
    Education= models.CharField(max_length=50,default='') #provide last course done by doctor like MBBS,MDBS
    specilist_type= models.CharField(max_length=12,default='') #doctor experties ex- cardiologist,dentist
    address_line_1=models.CharField(max_length=200,default='')
    address_line_2=models.CharField(max_length=200,default='')
    profile_pic=models.ImageField(upload_to='admin/image/profile_image',default='deafult_profile_pic.jpeg')
    is_verified=models.BooleanField(default=False)
    otp=models.CharField(max_length=200,default='')
    country_code=models.CharField(max_length=10)
    phone_number=models.CharField(max_length=15)
    country=models.CharField(max_length=100,default='')# ex- 91-india, 1-usa
    city=models.CharField(max_length=100,default='')
    state=models.CharField(max_length=100,default='')
    zip_code=models.CharField(max_length=100,default='') # this is the pincode or zipcode of aria
    is_user_blocked=models.BooleanField(default=False)
    timezone=models.TextField(default="UTC")
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['email', 'first_name','last_name','country_code','phone_number']
    objects=DoctorAccountManager()
    def has_perm(self, perm, obj=None):
        return self.is_admin
    def has_module_perms(self, app_label):
        return True

class AdminAccountManager(BaseUserManager):
    """Her we managed the all accounts from the django admin panel So before create account we need his info """
    def create_user(self, email,first_name,last_name,country_code,phone_number, password=None):
        if not email:
            raise 'User must have an Email'

        user =self.model(email=self.normalize_email(email),
                        first_name=first_name,
                        last_name=last_name,
                        country_code=country_code,
                        phone_number=phone_number)
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superadmin(self, email, first_name,last_name,country_code,phone_number,password=None):
        user = self.create_user(
			email=self.normalize_email(email),
			password=password,
            first_name=first_name,
            last_name=last_name,
			country_code=country_code,
			phone_number=phone_number,
		)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
class Admin(AbstractBaseUser):
    email=models.EmailField(verbose_name="email", max_length=60)
    username=models.CharField(verbose_name="nic name",max_length=30,default='')
    date_joined=models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login=models.DateTimeField(verbose_name='last login', auto_now=True)
    is_active=models.BooleanField(default=True)
    is_admin=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=True)
    is_superuser=models.BooleanField(default=False)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    user_type= models.CharField(max_length=12,default='Subadmin')#Subadmin, Receptionist etc
    address_line_1=models.CharField(max_length=200,default='')
    address_line_2=models.CharField(max_length=200,default='')
    profile_pic=models.ImageField(upload_to='user/image/profile_image',default='')
    is_verified=models.BooleanField(default=False)
    otp=models.CharField(max_length=200,default='')
    country_code=models.CharField(max_length=10)
    phone_number=models.CharField(max_length=15)
    country=models.CharField(max_length=100,default='')# ex- 91-india, 1-usa
    city=models.CharField(max_length=100,default='')
    state=models.CharField(max_length=100,default='')
    zip_code=models.CharField(max_length=100,default='') # this is the pincode or zipcode of aria
    is_user_blocked=models.BooleanField(default=False)
    timezone=models.TextField(default="UTC")
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['email', 'first_name','last_name','country_code','phone_number']
    objects=AdminAccountManager()
    def has_perm(self, perm, obj=None):
        return self.is_admin
    def has_module_perms(self, app_label):
        return True


class Admin_token(models.Model):
	admin=models.OneToOneField(Admin,on_delete=models.CASCADE,related_name='token')
	token=models.CharField(max_length=10,default='')
	def __str__(self):
		return 'ID='+str(self.id)+'user='+str(self.admin)+'token='+str(self.token)

class User_token(models.Model):
	user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='token')
	token=models.CharField(max_length=10,default='')
	def __str__(self):
		return 'ID='+str(self.id)+'user='+str(self.user)+'token='+str(self.token)

class Doctor_token(models.Model):
	doctor=models.OneToOneField(Doctor,on_delete=models.CASCADE,related_name='token')
	token=models.CharField(max_length=10,default='')
	def __str__(self):
		return 'ID='+str(self.id)+'user='+str(self.doctor)+'token='+str(self.token)