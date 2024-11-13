from sqlite3 import Date
from spyne import ComplexModel, Integer, Unicode, Double

class Client(ComplexModel):
    name = Unicode
    familyName = Unicode
    email = Unicode

class Account(ComplexModel) :
    rib  = Unicode
    client = Client
    balance = Double
    accountType = Unicode
    creationDate = Date

class Transaction (ComplexModel ) :
    id = Integer
    transactionTypes = Unicode
    account = Account
    transactionDate = Date
    amount = Double
    description = Unicode
    transfer_to_account = Unicode
