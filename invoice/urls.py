from django.urls import path, re_path
from . import views
app_name='invoice'
urlpatterns = [

path("invoice-<int:id>",views.invoice.as_view(),name='doctor'),

]