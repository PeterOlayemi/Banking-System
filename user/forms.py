from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *
import datetime

class LoginForm(forms.Form):
    user_id = forms.CharField(max_length=11, min_length=11, required=True, widget=forms.NumberInput(attrs= {'class':'form-control'}), label='User ID')
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs= {'class':'form-control'}))

class RegisterForm(UserCreationForm):
    phone_number = forms.CharField(max_length=11, min_length=11)
    area_code = forms.CharField(disabled=True, initial='+234')

    class Meta:
        model = User
        fields = ['first_name', 'middle_name', 'last_name', 'area_code', 'phone_number', 'email', 'password1', 'password2']

class CustomerAccountCreationForm(forms.ModelForm):
    bvn = forms.CharField(max_length=20, required=False, label='Bank Verification Number(Optional)')
    date_of_birth = forms.DateField(initial=datetime.date.today, widget=forms.widgets.DateInput(attrs={'type':'date'}))
    
    class Meta:
        model = CustomerAccount
        fields = ['account_type', 'bvn', 'date_of_birth', 'street_address', 'city', 'state', 'zip', 'country', 'marital_status', 'occupation']

class StaffAccountCreationForm(forms.ModelForm):
    date_of_birth = forms.DateField(initial=datetime.date.today, widget=forms.widgets.DateInput(attrs={'type':'date'}))
    
    class Meta:
        model = StaffAccount
        fields = ['street_address', 'city', 'state', 'zip', 'country', 'date_of_birth', 'marital_status', 'occupation']

class UpdateUserForm(forms.ModelForm):
    phone_number = forms.CharField(max_length=11, min_length=11)

    class Meta:
        model = User
        fields = ['first_name', 'middle_name', 'last_name', 'area_code', 'phone_number', 'email']
