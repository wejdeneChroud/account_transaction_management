from django.urls import path
from .views import bank_soap_app

urlpatterns = [
    path('soap/', bank_soap_app), 
]
