from django.db import models
from django.utils import timezone
import secrets

from user.models import *
from .paystack import Paystack

# Create your models here.

CARD_TYPE = (
    ('VISA', 'VISA'),
    ('Verve', 'Verve'),
    ('MasterCard', 'MasterCard'),
    )

TXN = (
    ('Debit', 'Debit'),
    ('Credit', 'Credit')
    )

HOW = (
    ('Mobile', 'Mobile'),
    ('Card', 'Card'),
    ('USSD', 'USSD'),
    ('ATM', 'ATM'),
    )

WHICH = (
    ('UTU', 'UTU'),
    ('UTO', 'UTO'),
    ('Patridge Bank', 'Patridge Bank'),
    ('TOPUP', 'TOPUP'),
    ('BILL', 'BILL'),
    )

PERIOD = (
    ('1 Week', '1 Week'),
    ('1 Month', '1 Month'),
    ('3 Months', '3 Months'),
    ('6 Months', '6 Months'),
)

class Exchange(models.Model):
    currency = models.CharField(max_length=3)
    buy = models.FloatField(default=0.00)
    mid = models.FloatField(default=0.00)
    sell = models.FloatField(default=0.00)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.currency}'

class NewsManager(models.Manager):
    def read_news(self, user_id, news_id):
        news = super(NewsManager, self).get(pk=news_id)
        news.read.add(user_id)
        return news
    
class News(models.Model):
    read = models.ManyToManyField(User, blank=True, related_name='user')
    title = models.CharField(max_length=299)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    objects = NewsManager()

    def __str__(self):
        return f'{self.title}'

class AlertManager(models.Manager):
    def read_alert(self, alert_id):
        alert = super(AlertManager, self).get(pk=alert_id)
        alert.read = True
        alert.save()
        return alert

class Alert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    read = models.BooleanField(default=False)
    transfer = models.ForeignKey('Transfer', on_delete=models.CASCADE, blank=True, null=True)
    bill = models.ForeignKey('Bill', on_delete=models.CASCADE, blank=True, null=True)
    topup = models.ForeignKey('TopUp', on_delete=models.CASCADE, blank=True, null=True)
    card = models.ForeignKey('Card', on_delete=models.CASCADE, blank=True, null=True)
    loan = models.ForeignKey('Loan', on_delete=models.CASCADE, blank=True, null=True)
    modify_limit = models.BooleanField(default=False)
    statement = models.BooleanField(default=False)
    txn = models.CharField(max_length=9, choices=TXN)
    how = models.CharField(max_length=49, choices=HOW)
    which = models.CharField(max_length=49, choices=WHICH)
    detail = models.CharField(max_length=299)
    amount = models.FloatField(default=0.00)
    balance = models.FloatField(default=0.00)
    date = models.DateTimeField(auto_now_add=True)
    
    objects = AlertManager()

    def __str__(self):
        return f'{self.txn} on {self.user}'

class Transfer(models.Model):
    user = models.ManyToManyField(User)
    sender = models.ForeignKey(CustomerAccount, on_delete=models.SET_NULL, null=True, related_name='sender', db_index=True)
    receiver = models.ForeignKey(CustomerAccount, on_delete=models.SET_NULL, null=True, related_name='receiver', db_index=True)
    txn_id = models.CharField(max_length=15)
    amount = models.FloatField(default=0.00)
    purpose = models.CharField(max_length=19, blank=True, null=True)
    status = models.CharField(max_length=19, default='Processing')
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Status - {self.status}: {self.sender.account_name} to {self.receiver.account_name}'

class CableService(models.Model):
    name = models.CharField(max_length=99)
    
    def __str__(self):
        return self.name

class CablePlan(models.Model):
    service = models.ForeignKey(CableService, on_delete=models.CASCADE)
    name = models.CharField(max_length=299)
    amount = models.FloatField(default=0.00)
    product_code = models.CharField(max_length=49)

    def __str__(self):
        return f'{self.name}'

class Cable(models.Model):
    account = models.ForeignKey(CustomerAccount, on_delete=models.CASCADE, db_index=True)
    service = models.ForeignKey(CableService, on_delete=models.SET_NULL, null=True)
    plan = models.ForeignKey(CablePlan, on_delete=models.SET_NULL, blank=True, null=True)
    customer_name = models.CharField(max_length=99, blank=True, null=True)
    customer_number = models.CharField(max_length=30, blank=True, null=True)
    card_number = models.CharField(max_length=30)
    exchange_reference = models.CharField(max_length=99, blank=True, null=True)
    customercare_referenceid = models.CharField(max_length=99, blank=True, null=True)
    audit_referencenumber = models.CharField(max_length=99, blank=True, null=True)
    
    def __str__(self):
        return f"{self.account.account_name}"

class ElectricityService(models.Model):
    name = models.CharField(max_length=99)
    
    def __str__(self):
        return self.name

class Electricity(models.Model):
    account = models.ForeignKey(CustomerAccount, on_delete=models.CASCADE, db_index=True)
    service = models.ForeignKey(ElectricityService, on_delete=models.SET_NULL, null=True)
    meter_number = models.CharField(max_length=19)
    customer_name = models.CharField(max_length=99)
    customer_district = models.CharField(max_length=99, blank=True, null=True)
    customer_reference = models.CharField(max_length=99, blank=True, null=True)
    customer_address = models.CharField(max_length=99)
    amount = models.FloatField(default=0.00)
    tariff_code = models.CharField(max_length=99, blank=True, null=True)
    phone_number = models.CharField(max_length=11, blank=True, null=True)
    bsst_tokenvalue = models.CharField(max_length=99, blank=True, null=True)
    standard_tokenvalue = models.CharField(max_length=99, blank=True, null=True)
    utility_name = models.CharField(max_length=99, blank=True, null=True)
    exchange_reference = models.CharField(max_length=99, blank=True, null=True)
    token = models.CharField(max_length=99, blank=True, null=True)
    unit = models.CharField(max_length=99, blank=True, null=True)
    receipt_number = models.CharField(max_length=99, blank=True, null=True)
    
    def __str__(self):
        return f"{self.account.account_name}"

class Provider(models.Model):
    name = models.CharField(max_length=99, db_index=True)
    
    def __str__(self):
        return self.name

class Airtime(models.Model):
    account = models.ForeignKey(CustomerAccount, on_delete=models.CASCADE, db_index=True)
    date = models.DateTimeField(auto_now_add=True)
    service = models.ForeignKey(Provider, on_delete=models.SET_NULL, null=True)
    amount = models.FloatField()
    phone_number = models.CharField(max_length=11)
    
    def __str__(self):
        return f"{self.account.account_name}"

class Plan(models.Model):
    service = models.ForeignKey(Provider, on_delete=models.CASCADE)
    name = models.CharField(max_length=99)
    amount = models.FloatField(default=0.0)
    product_code = models.CharField(max_length=49)
    
    def __str__(self):
        return self.name

class Data(models.Model):
    account = models.ForeignKey(CustomerAccount, on_delete=models.CASCADE, db_index=True)
    service = models.ForeignKey(Provider, on_delete=models.SET_NULL, null=True)
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True)
    phone_number = models.CharField(max_length=11)
    
    def __str__(self):
        return f"{self.account.account_name}"

class Bill(models.Model):
    saved = models.BooleanField(default=False)
    status = models.CharField(max_length=100, default='Processing')
    txn_id = models.CharField(max_length=15)
    account = models.ForeignKey(CustomerAccount, on_delete=models.CASCADE, db_index=True)
    cable = models.ForeignKey(Cable, on_delete=models.CASCADE, related_name='cable', blank=True, null=True)
    electricity = models.ForeignKey(Electricity, on_delete=models.CASCADE, related_name='electricity', blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.account.account_name

class TopUp(models.Model):
    saved = models.BooleanField(default=False)
    status = models.CharField(max_length=100, default='Processing')
    txn_id = models.CharField(max_length=15)
    account = models.ForeignKey(CustomerAccount, on_delete=models.CASCADE, db_index=True)
    airtime = models.ForeignKey(Airtime, on_delete=models.CASCADE, related_name='airtime', blank=True, null=True)
    data = models.ForeignKey(Data, on_delete=models.CASCADE, related_name='data', blank=True, null=True)
    amount = models.FloatField()
    phone_number = models.CharField(max_length=11)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.account.account_name

class Beneficiary(models.Model):
    confirm = models.BooleanField(default=False)
    account = models.ForeignKey(CustomerAccount, on_delete=models.CASCADE, related_name = 'account', db_index=True)
    beneficiary = models.ForeignKey(CustomerAccount, on_delete=models.CASCADE, related_name = 'beneficiary', db_index=True)

    def __str__(self):
        return f'{self.beneficiary.account_name} - beneficiary of {self.account.account_name}'

class Txn(models.Model):
    account = models.ForeignKey(CustomerAccount, on_delete=models.CASCADE, db_index=True)
    transfer = models.ForeignKey(Transfer, on_delete=models.CASCADE, blank=True, null=True)
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, blank=True, null=True)
    topup = models.ForeignKey(TopUp, on_delete=models.CASCADE, blank=True, null=True)
    amount = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.account.account_name}'
    
class Card(models.Model):
    card_id = models.CharField(max_length=15)
    account = models.ForeignKey(CustomerAccount, on_delete=models.CASCADE, db_index=True)
    card_type = models.CharField(max_length=19, choices=CARD_TYPE)
    card = models.CharField(max_length=9, choices=TXN)
    card_number = models.CharField(max_length=16)
    cvv = models.CharField(max_length=3)
    expires = models.DateField()
    pin = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.account.account_name}'

class Loan(models.Model):
    paid = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    disapproved = models.BooleanField(default=False)
    account = models.ForeignKey(CustomerAccount, on_delete=models.CASCADE, db_index=True)
    reason = models.CharField(max_length=299)
    amount = models.FloatField(default=0.00)
    new_amount = models.FloatField(default=0.00, blank=True, null=True)
    source_of_income = models.CharField(max_length=99)
    period = models.CharField(max_length=99, choices=PERIOD)
    till = models.DateField(blank=True, null=True)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.account.account_name}; Approved: {self.approved}; Disapproved: {self.disapproved}'

class Wallet(models.Model):
    completed = models.BooleanField(default=False)
    account = models.ForeignKey(CustomerAccount, on_delete=models.CASCADE)
    amount = models.FloatField(default=0.00)
    email = models.EmailField()
    ref = models.CharField(max_length=199)
    date_created = models.DateTimeField(auto_now_add=True)
    date_completed = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
         return f"Funding: {self.price} by {self.account.account_name}"

    def save(self, *args, **kwargs):
        while not self.ref:
            ref = secrets.token_urlsafe(50)
            object_with_similar_ref = Wallet.objects.filter(ref=ref)
            if not object_with_similar_ref:
                self.ref = ref

        super().save(*args, **kwargs)
	
    def price_value(self):
        return int(self.amount) * 100

    def verify_payment(self):
        paystack = Paystack()
        status, result = paystack.verify_payment(self.ref, self.amount)
        if status:
            if result['amount'] / 100 == self.amount:
                self.completed = True
                self.date_completed = timezone.now()
            self.save()
        if self.completed:
            return True
        return False
