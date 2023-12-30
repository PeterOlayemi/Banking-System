from django import forms
import datetime
from .models import *

class CableForm(forms.ModelForm):
    card_number = forms.CharField(max_length=10, min_length=10)

    class Meta:
        model= Cable
        fields=['service', 'plan', 'card_number']
        labels={}

class ElectricityForm(forms.ModelForm):
    
    class Meta:
        model= Electricity
        fields=['service', 'meter_number', 'amount', 'phone_number']
        labels={}

class AirtimeForm(forms.ModelForm):
    service = forms.ChoiceField(choices=[])  # Placeholder for the choices

    class Meta:
        model= Airtime
        fields=['service', 'amount', 'phone_number']
        labels={}

    def clean_service(self):
        service_id = self.cleaned_data['service']
        provider_instance = Provider.objects.get(name=service_id)
        return provider_instance

    def __init__(self, *args, **kwargs):
        provider_statuses = kwargs.pop('provider_statuses', {})  # Get the service_statuses passed as a keyword argument
        super(AirtimeForm, self).__init__(*args, **kwargs)

        # Create a list of choices for the dropdown field using service names and statuses
        choices =[('', 'Choose a Service')] + [(provider_name, f"{provider_name} ({status})") for provider_name, status in provider_statuses.items()]

        # Set the choices for the service_dropdown field
        self.fields['service'].choices = choices

class DataForm(forms.ModelForm):
    service = forms.ChoiceField(choices=[])
    
    class Meta:
        model= Data
        fields=['service', 'plan', 'phone_number']
        labels={}

    def clean_service(self):
        service_id = self.cleaned_data['service']
        provider_instance = Provider.objects.get(id=service_id)
        return provider_instance

    def __init__(self, *args, **kwargs):
        provider_statuses = kwargs.pop('provider_statuses', {})  # Get the service_statuses passed as a keyword argument
        super(DataForm, self).__init__(*args, **kwargs)

        # Create a list of choices for the dropdown field using service names and statuses
        choices = [('', 'Choose a Service')] + [(id_provider, f"{provider_name} ({status})")
                   for id_provider, (provider_name, status) in provider_statuses.items()]

        # Set the choices for the service_dropdown field
        self.fields['service'].choices = choices
        try:
            service_id = int(self.data.get('service'))
            if service_id:
                self.fields['plan'].queryset = Plan.objects.filter(service_id=service_id).all()
            else:
                self.fields['plan'].queryset = Plan.objects.none()
        except (TypeError):
            self.fields['plan'].queryset = Plan.objects.none()
        
class PictureForm(forms.Form):
    picture = forms.ImageField(label='')

class FundForm(forms.ModelForm):
    class Meta:
        model = Wallet
        fields = ['email', 'amount']
