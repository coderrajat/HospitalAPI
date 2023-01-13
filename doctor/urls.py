from django.urls import path, re_path
from . import views
app_name='doctor'
urlpatterns = [
    path("doctor_details",views.Doctor_details.as_view(),name='doctor'),
    path("Appointment",views.Appointment.as_view(),name='Appointment')
]