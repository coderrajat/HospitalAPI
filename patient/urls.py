from django.urls import path, re_path
from . import views
urlpatterns = [
    path("Patient/patient_details",views.Patientdetails.as_view(),name='appointment'),
    # path("Appointment",views.Appointment.as_view(),name='Appointment')
]