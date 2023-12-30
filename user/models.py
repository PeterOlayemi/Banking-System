from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from django_countries.fields import CountryField

# Create your models here.

STATE = (
    ('Abia', 'Abia'),
    ('Adamawa', 'Adamawa'),
    ('Akwa Ibom', 'Akwa Ibom'),
    ('Anambra', 'Anambra'),
    ('Bauchi', 'Bauchi'),
    ('Bayelsa', 'Bayelsa'),
    ('Benue', 'Benue'),
    ('Borno', 'Borno'),
    ('Cross River', 'Cross River'),
    ('Delta', 'Delta'),
    ('Ebonyi', 'Ebonyi'),
    ('Edo', 'Edo'),
    ('Ekiti', 'Ekiti'),
    ('Enugu', 'Enugu'),
    ('Gombe', 'Gombe'),
    ('Imo', 'Imo'),
    ('Jigawa', 'Jigawa'),
    ('Kaduna', 'Kaduna'),
    ('Kano', 'Kano'),
    ('Katsina', 'Katsina'),
    ('Kebbi', 'Kebbi'),
    ('Kogi', 'Kogi'),
    ('Kwara', 'Kwara'),
    ('Lagos', 'Lagos'),
    ('Nasarawa', 'Nasarawa'),
    ('Niger', 'Niger'),
    ('Ogun', 'Ogun'),
    ('Ondo', 'Ondo'),
    ('Osun', 'Osun'),
    ('Oyo', 'Oyo'),
    ('Plateau', 'Plateau'),
    ('Rivers', 'Rivers'),
    ('Sokoto', 'Sokoto'),
    ('Taraba', 'Taraba'),
    ('Yobe', 'Yobe'),
    ('Zamfara', 'Zamfara'),
    ('FCT', 'FCT'),
)

ACCOUNT_TYPE = (
    ('Savings', 'Savings'),
    ('Current', 'Current')
    )

MARITAL_STATUS = (
    ('Married', 'Married'),
    ('Single', 'Single'),
    ('Divorced', 'Divorced'),
    ('Widowed', 'Widowed'),
    ('Separated', 'Separated'),
    )

class UserManager(BaseUserManager):

    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        user = self._create_user(email, password, True, True, **extra_fields)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    is_staff = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)

    email_notification = models.BooleanField(default=False)
    balance = models.FloatField(default=0.00)
    first_name = models.CharField(max_length=99)
    middle_name = models.CharField(max_length=99)
    last_name = models.CharField(max_length=99)
    area_code = models.CharField(max_length=4, default='+234')
    phone_number = models.CharField(max_length=11, unique=True)
    email = models.EmailField(max_length=249)
    user_ID = models.CharField(max_length=11, unique=True, blank=True, null=True, db_index=True)
    pin = models.CharField(max_length=4, blank=True, null=True)

    USERNAME_FIELD = 'user_ID'
    EMAIL_FIELD = 'email'

    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def __str__(self):
        return f'{self.first_name} {self.middle_name} {self.last_name}'

class CustomerAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=10, unique=True, db_index=True)
    account_name = models.CharField(max_length=299, db_index=True)
    txn_limit = models.FloatField(default=100000)
    
    picture = models.ImageField(upload_to='img/')
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPE)
    bvn = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField()
    street_address = models.CharField(max_length=99)
    city = models.CharField(max_length=99)
    state = models.CharField(max_length=99, choices=STATE)
    zip = models.CharField(max_length=9)
    country = CountryField(multiple=False)
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS)
    occupation = models.CharField(max_length=99)

    def __str__(self):
        return f'{self.account_name}'

class StaffAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_name = models.CharField(max_length=299, db_index=True)
    
    picture = models.ImageField(upload_to='img/')
    date_of_birth = models.DateField()
    street_address = models.CharField(max_length=99)
    city = models.CharField(max_length=99)
    state = models.CharField(max_length=99, choices=STATE)
    zip = models.CharField(max_length=9)
    country = CountryField(multiple=False)
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS)
    occupation = models.CharField(max_length=99)

    def __str__(self):
        return f'{self.account_name}'

class MessageManager(models.Manager):
    def read_message(self, message_id):
        message = super(MessageManager, self).get(pk=message_id)
        message.read = True
        message.save()
        return message
    
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    message = models.CharField(max_length=299)
    date = models.DateTimeField(auto_now_add=True)

    objects = MessageManager()

    def __str__(self):
        return f'{self.message} - {self.user}'
