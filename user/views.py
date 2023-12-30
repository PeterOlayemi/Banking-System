from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from .token import account_activation_token
from django.core.mail import BadHeaderError, EmailMultiAlternatives
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import PasswordResetForm
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
import random
from django.utils import timezone

from .models import *
from .forms import  *
from customer.views import *

# Create your views here.

def random_account_number():
    return int(random.uniform(1000000000, 9999999999))

def generate_account_number():
    while True:
        account_number = random_account_number()
        if not CustomerAccount.objects.filter(account_number=account_number).exists():
            return account_number

def CustomerLoginView(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user_id = request.POST['user_id']
            password = request.POST['password']
            user = authenticate(request, username=user_id, password=password)
            if user is not None and user.is_customer == True:
                login(request, user)
                
                UpdateGOTVPackageView()
                UpdateDSTVPackageView()
                UpdateStartimesPackageView()

                UpdateElectricityBillerView()
                
                UpdateMTNPlanView()
                UpdateEtisalatPlanView()
                UpdateGLOPlanView()
                UpdateAIRTELPlanView()
                
                if 'remember_me' in request.POST:
                    request.session.set_expiry(60*60*24)
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                else:
                    return redirect('customer_home')
            else:
                messages.error(request, 'Invalid User ID Or Password')
                return redirect('customer_login')
    else:
        form = LoginForm()
    context = {'form':form}
    return render(request, 'customer/login.html', context)

def StaffLoginView(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user_id = request.POST['user_id']
            password = request.POST['password']
            user = authenticate(request, username=user_id, password=password)
            if user is not None and user.is_staff == True:
                login(request, user)
                
                UpdateGOTVPackageView()
                UpdateDSTVPackageView()
                UpdateStartimesPackageView()

                UpdateElectricityBillerView()

                UpdateMTNPlanView()
                UpdateEtisalatPlanView()
                UpdateGLOPlanView()
                UpdateAIRTELPlanView()
                
                if 'remember_me' in request.POST:
                    request.session.set_expiry(60*60*24)
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                else:
                    return redirect('staff_home')
            else:
                messages.error(request, 'Invalid User ID Or Password')
                return redirect('staff_login')
    else:
        form = LoginForm()
    context = {'form':form}
    return render(request, 'staff/login.html', context)

def CustomerRegisterView(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.is_customer = True
            user.save()
            current_site = get_current_site(request)
            subject = 'Patridge Bank: Notification to verify email'
            email_template_name = 'mail/acc_activate.txt'
            context = {
            'domain': current_site.domain,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "user": user,
            'token': account_activation_token.make_token(user),
            }
            email = render_to_string(email_template_name, context)
            try:
                msg = EmailMultiAlternatives(subject, email, settings.EMAIL_HOST_USER, [user.email])
                msg.send()
            except BadHeaderError:
                return redirect('Invalid header found.')
            messages.success(request, 'Verify Your Email To Continue.<br>Please Check Your Email Inbox Or Spam To Confirm Your Email Address.')
            return redirect('customer_login')
    return render(request, 'customer/register.html', {'form':form})

def StaffRegisterView(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.is_staff = True
            user.save()
            current_site = get_current_site(request)
            subject = 'Patridge Bank: Notification To Verify Email'
            email_template_name = 'mail/acc_activate.txt'
            context = {
            'domain': current_site.domain,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "user": user,
            'token': account_activation_token.make_token(user),
            }
            email = render_to_string(email_template_name, context)
            try:
                msg = EmailMultiAlternatives(subject, email, settings.EMAIL_HOST_USER, [user.email])
                msg.send()
            except BadHeaderError:
                return redirect('Invalid header found.')
            messages.success(request, 'Verify Your Email To Continue.<br>Please Check Your Email Inbox Or Spam To Confirm Your Email Address.')
            return redirect('staff_login')
    return render(request, 'staff/register.html', {'form':form})

def CustomerCreateAccountView(request, pk):
    user = User.objects.get(id=pk)
    if request.method == 'POST':
        form = CustomerAccountCreationForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = user
            data.id = user.id
            data.account_name = user.first_name + ' ' + user.middle_name + ' ' + user.last_name
            data.account_number = generate_account_number()
            try:
                agree = request.POST['agree']
            except (KeyError, UnboundLocalError):
                messages.error(request, 'Kindly Agree To Our Terms And Policies Before You Continue!')
                return redirect(reverse('customer_create', args=[user.pk]))
            else:
                data.save()
                messages.success(request, 'Information Saved')
                return redirect(reverse('addpin', args=[user.pk]))
    else:
        form = CustomerAccountCreationForm()
    return render(request, 'general/createaccount.html', {'form':form})

def StaffCreateAccountView(request, pk):
    user = User.objects.get(id=pk)
    if request.method == 'POST':
        form = StaffAccountCreationForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = user
            data.id = user.id
            data.account_name = user.first_name + ' ' + user.middle_name + ' ' + user.last_name
            try:
                agree = request.POST['agree']
            except (KeyError, UnboundLocalError):
                messages.error(request, 'Kindly Agree To Our Terms And Policies Before You Continue!')
                return redirect(reverse('staff_create', args=[user.pk]))
            else:
                user.user_ID = user.phone_number
                user.save()
                data.save()
                subject = 'Patridge Bank: Account Creation Successful'
                email_template_name = 'mail/staff_acc_creation.txt'
                current_site = get_current_site(request)
                context = {
                'domain': current_site.domain,
                "user": user,
                "data": data,
                }
                email = render_to_string(email_template_name, context)
                try:
                    msg = EmailMultiAlternatives(subject, email, settings.EMAIL_HOST_USER, [user.email])
                    msg.send()
                except BadHeaderError:
                    return redirect('Invalid header found.')
                messages.success(request, 'Account Creation Successful. A Success Email Has Been Sent To Your Inbox. You Can Login Now')
                return redirect('staff_login')
    else:
        form = StaffAccountCreationForm()
    return render(request, 'general/createaccount.html', {'form':form, 'staff':'staff'})

def AddPinView(request, pk):
    user = User.objects.get(id=pk)
    data = CustomerAccount.objects.get(id=user.id)
    if request.method == 'POST':
        pin = request.POST['pin']
        post = User.objects.filter(pin=pin)
        if post.exists():
            messages.error(request, 'Pin Is Too Common')
            return redirect(reverse('addpin', args=[user.pk]))
        if pin == '0000' or pin == '1234' or pin == '1111' or pin == '2222' or pin == '3333' or pin == '4444' or pin == '5555' or pin == '6666' or pin == '7777' or pin == '8888' or pin == '9999':
            messages.error(request, 'Pin Is Too Common')
            return redirect(reverse('addpin', args=[user.pk]))
        user.user_ID = user.phone_number
        user.pin = pin
        try:
            user.save()
        except(ValueError):
            messages.error(request, 'Pin Should Be Digits')
            return redirect(reverse('addpin', args=[user.pk]))
        subject = 'Patridge Bank: Account Creation Successful'
        email_template_name = 'mail/customer_acc_creation.txt'
        current_site = get_current_site(request)
        context = {
        'domain': current_site.domain,
        "user": user,
        "data": data,
        }
        email = render_to_string(email_template_name, context)
        try:
            msg = EmailMultiAlternatives(subject, email, settings.EMAIL_HOST_USER, [user.email])
            msg.send()
        except BadHeaderError:
            return redirect('Invalid header found.')
        message = Message(user=user, message=f'Patridge Bank: Account Creation Successful. Welcome {data.account_name}')
        message.save()
        messages.success(request, 'Account Creation Successful. A Success Email Has Been Sent To Your Inbox. You Can Login Now')
        return redirect('customer_login')
    return render(request, 'customer/addpin.html')

def TermView(request):
    return render(request, 'general/term.html')

def PrivacyView(request):
    return render(request, 'general/privacy.html')

def CustomerPasswordResetRequestView(request):
    form = PasswordResetForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            data = form.cleaned_data['email']
            user = User.objects.filter(email=data)
            if user.exists():
                for user in user:
                    current_site = get_current_site(request)
                    subject = "Patridge Bank: Password Reset Request"
                    email_template_name = "mail/customer_password_reset_email.txt"
                    context = {
                    'domain': current_site.domain,
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
                    'date': timezone.now().date(),
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
                    email = render_to_string(email_template_name, context)
                    try:
                        msg = EmailMultiAlternatives(subject, email, settings.EMAIL_HOST_USER, [user.email])
                        msg.send()
                    except BadHeaderError:
                        return redirect('Invalid header found.')
                    messages.success(request, 'Please Check Your Email Inbox Or Spam For Instructions On How To Reset Your Password')
                    return redirect('customer_login')
            else:
                messages.error(request, 'Email Not Found')
                return redirect("customer_password_reset")
    return render(request, "customer/password_reset.html", context={"form":form})

def StaffPasswordResetRequestView(request):
    form = PasswordResetForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            data = form.cleaned_data['email']
            user = User.objects.filter(email=data)
            if user.exists():
                for user in user:
                    current_site = get_current_site(request)
                    subject = "Patridge Bank: Password Reset Request"
                    email_template_name = "mail/staff_password_reset_email.txt"
                    context = {
                    'domain': current_site.domain,
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
                    'date': timezone.now().date(),
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
                    email = render_to_string(email_template_name, context)
                    try:
                        msg = EmailMultiAlternatives(subject, email, settings.EMAIL_HOST_USER, [user.email])
                        msg.send()
                    except BadHeaderError:
                        return redirect('Invalid header found.')
                    messages.success(request, 'Please Check Your Email Inbox Or Spam For Instructions On How To Reset Your Password')
                    return redirect('staff_login')
            else:
                messages.error(request, 'Email Not Found')
                return redirect("staff_password_reset")
    return render(request, "staff/password_reset.html", context={"form":form})

def ActivateAccountView(request, uidb64, token):
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True
        user.save()
        if user.is_customer:
            messages.success(request, 'Your Email Has Been Confirmed. Continue Setup Below')
            return redirect(reverse('customer_create', args=[user.pk]))
        elif user.is_staff:
            messages.success(request, 'Your Email Has Been Confirmed. Continue Setup Below')
            return redirect(reverse('staff_create', args=[user.pk]))
    else:
        if user.is_customer:
            messages.error(request, 'Activation Link Is Invalid!')
            return redirect('customer_login')
        elif user.is_staff:
            messages.error(request, 'Activation Link Is Invalid!')
            return redirect('staff_login')

def StaffLogOutView(request):
    logout(request)
    return redirect('staff_login')

def CustomerLogOutView(request):
    logout(request)
    return redirect('customer_login')
