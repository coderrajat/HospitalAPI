from django.contrib import admin
from . import models
from django.contrib.auth.admin import UserAdmin

class AccountAdmin(UserAdmin):
	list_display = ('email', 'first_name','last_name','date_joined', 'last_login', 'is_admin', 'is_staff')
	search_fields = ('email', )
	readonly_fields = ('date_joined', 'last_login')

	filter_horizontal = ()
	list_filter = ()
	fieldsets = ()

admin.site.register(models.User)
admin.site.register(models.Doctor)
admin.site.register(models.Admin)
admin.site.register(models.Admin_token)
admin.site.register(models.User_token)
admin.site.register(models.Doctor_token)

# Register your models here.
