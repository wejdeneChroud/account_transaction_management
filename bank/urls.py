from django.urls import path
from .views import bank_soap_app, ui_view, get_account_details, get_all_accounts

urlpatterns = [
    path('soap/', bank_soap_app),
    path('', ui_view, name='ui_view'),
    path('get_account_details/', get_account_details, name='get_account_details'),
    path('get_all_accounts/', get_all_accounts, name='get_all_accounts'),

]
