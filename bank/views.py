from spyne.service import ServiceBase
from spyne.decorator import rpc
from spyne.model.primitive import Unicode
from spyne.application import Application
from spyne.protocol.soap import Soap11
from spyne.server.django import DjangoApplication

from spyne.model.complex import Iterable
from django.views.decorators.csrf import csrf_exempt
from .complexTypes import Account as complexAccount
from .models import Account as modelAccount, Client as modelClient

class AccountService(ServiceBase):
    @rpc(complexAccount, _returns=Unicode)
    def add_account(self, account):
        if modelAccount.objects.filter(pk=account.rib).exists():
            return 'This account already exists'
        #verify if the client already exists
        try:
            client=modelClient.objects.get(pk=account.client.cin)
        except modelClient.DoesNotExist:

                #create a new Client instance
                client=modelClient(account.client.cin, account.client.name,account.client.familyName,account.client.email)
                #insert the client into the DB
                client.save()
            #convert the account ComplexType into Model Account
        acc=modelAccount()
        acc.rib=account.rib
        acc.client=client
        acc.balance=account.balance
        acc.creation_date=account.creationDate
        acc.save()
        return 'The account with RIB {account.rib} is successfully created.'

    @rpc(Unicode,_returns=complexAccount)
    def get_account_details(self, email:str)-> complexAccount:
        account=modelAccount.objects.filter(client__email__iexact=email).first()
        if account is None:
            raise ValueError(f'There is no account for email {email}')
        #convert for Model Account to complexType Account
        complexAcc=complexAccount()
        complexAcc.rib=account.rib
        complexAcc.client=account.client
        complexAcc.balance=account.balance
        complexAcc.creationDate=account.creation_date
        return complexAcc
    @rpc(_returns=Iterable(complexAccount))
    def get_all_accounts(self):
        accounts=modelAccount.objects.all()
        #convert for Model Accounts to an iterable of complex type Accounts
        for account in accounts:
            complexAcc=complexAccount(
                rib=account.rib,
                client=account.client,
                balance=account.balance,
                creationDate=account.creation_date
            )
            yield complexAcc

#Configuration of The SOAP API
application=Application(
    [AccountService],
    tns='bank.isg.tn',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)
django_app=DjangoApplication(application)
bank_soap_app=csrf_exempt(django_app)