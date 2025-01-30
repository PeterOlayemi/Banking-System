from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site  
from django.template.loader import render_to_string  
from django.core.mail import BadHeaderError, EmailMultiAlternatives
from django.conf import settings
from django.contrib.auth.forms import SetPasswordForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import datetime
from django.db.models import Q, Count
from django.http import FileResponse
from django.utils import timezone
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


from .models import *
from user.models import *
from customer.models import *
from .forms import  *
from user.forms import *
from customer.forms import *
from user.views import *
from customer.views import *

# Create your views here.

def date_eligible(account):
    return account.user.date_joined + datetime.timedelta(weeks=24)

def transaction_eligible(account):
    if Txn.objects.filter(account=account).exists():
        txn = Txn.objects.filter(account=account)
        trans = [float(tin.amount) for tin in txn]
        return sum(trans)
    else:
        return 0

@staff_member_required(login_url='staff_login')
def SHomeView(request):
    unread_conversation = Conversation.objects.annotate(
        unread_messages_count = Count('chat', filter=~Q(chat__sender=request.user) & Q(chat__read=False))
    ).filter(
        participants=request.user,
        unread_messages_count__gt=0
    ).count()
    support_count = Support.objects.filter(answer=False).exclude(staff__in=User.objects.filter(is_staff=True)).exclude(staff__in=User.objects.filter(is_customer=True)).count()
    return render(request, 'staff/home.html', {'unread_conversation':unread_conversation, 'support_count':support_count})

@staff_member_required(login_url='staff_login')
def SProfileView(request):
    unread_conversation = Conversation.objects.annotate(
        unread_messages_count = Count('chat', filter=~Q(chat__sender=request.user) & Q(chat__read=False))
    ).filter(
        participants=request.user,
        unread_messages_count__gt=0
    ).count()
    account = StaffAccount.objects.get(user=request.user)
    if request.method == 'POST':
        form = PictureForm(request.POST, request.FILES)
        if form.is_valid():
            account.picture = form.cleaned_data['picture']
            account.save()
            messages.success(request, 'Picture Added Successfully')
            return redirect('sprofile')
    else:
        form = PictureForm()
    return render(request, 'staff/profile.html', {'unread_conversation':unread_conversation, 'account':account, 'form':form})

@staff_member_required(login_url='staff_login')
def EditProfileView(request):
    unread_conversation = Conversation.objects.annotate(
        unread_messages_count = Count('chat', filter=~Q(chat__sender=request.user) & Q(chat__read=False))
    ).filter(
        participants=request.user,
        unread_messages_count__gt=0
    ).count()
    account = StaffAccount.objects.get(user=request.user)
    if request.method == 'POST':
        form1 = UpdateUserForm(request.POST, instance=account.user)
        form2 = StaffAccountCreationForm(request.POST, instance=account)
        if form1.is_valid() and form2.is_valid():
            form1.save()
            form2.save()
            messages.success(request, 'Profile Saved')
            return redirect('sprofile')
    else:
        form1 = UpdateUserForm(instance=account.user)
        form2 = StaffAccountCreationForm(instance=account)
    return render(request, 'staff/editprofile.html', {'unread_conversation':unread_conversation, 'form1':form1, 'form2':form2, 'account':account})

@staff_member_required(login_url='staff_login')
def SChangeUserIDView(request):
    unread_conversation = Conversation.objects.annotate(
        unread_messages_count = Count('chat', filter=~Q(chat__sender=request.user) & Q(chat__read=False))
    ).filter(
        participants=request.user,
        unread_messages_count__gt=0
    ).count()
    account = StaffAccount.objects.get(user=request.user)
    if request.method == 'POST':
        if request.POST['old_user_id'] != account.user.user_ID:
            messages.error(request, 'Wrong User ID')
            return redirect('schangeuserid')
        if len(request.POST['new_user_id']) > 11 or len(request.POST['new_user_id']) < 11:
            messages.error(request, 'Length Of User ID Should Be 11 Digits')
            return redirect('schangeuserid')
        else:
            account.user.user_ID = request.POST['new_user_id']
            account.user.save()
            messages.success(request, 'User ID Changed Successfully')
            return redirect('staff_home')
    return render(request, 'staff/changeuserid.html', {'unread_conversation':unread_conversation})

@staff_member_required(login_url='staff_login')
def CreateCustomerView(request):
    unread_conversation = Conversation.objects.annotate(
        unread_messages_count = Count('chat', filter=~Q(chat__sender=request.user) & Q(chat__read=False))
    ).filter(
        participants=request.user,
        unread_messages_count__gt=0
    ).count()
    form1 = RegisterForm(request.POST or None)
    form2 = CustomerAccountCreationForm(request.POST or None)
    if request.method == 'POST':
        if form1.is_valid() and form2.is_valid():
            data1 = form1.save(commit=False)
            data1.is_customer = True
            data1.save()
            data2 = form2.save(commit=False)
            data2.user = data1
            data2.id = data1.id
            data2.account_name = data1.first_name + ' ' + data1.middle_name + ' ' + data1.last_name
            data2.account_number = generate_account_number()
            data2.save()
            pin = request.POST['pin']
            post = User.objects.filter(pin=pin)
            if post.exists():
                messages.error(request, 'Pin Is Too Common')
                return redirect('createcustomer')
            if pin == '0000' or pin == '1234' or pin == '1111' or pin == '2222' or pin == '3333' or pin == '4444' or pin == '5555' or pin == '6666' or pin == '7777' or pin == '8888' or pin == '9999':
                messages.error(request, 'Pin Is Too Common')
                return redirect('createcustomer')
            data1.user_ID = data1.phone_number
            data1.pin = pin
            try:
                data1.save()
            except(ValueError):
                messages.error(request, 'Pin Should Be Digits')
                return redirect('createcustomer')
            subject = 'Patridge Bank: Account Creation Successful'
            email_template_name = 'mail/customer_acc_creation.txt'
            current_site = get_current_site(request)
            context = {
            'domain': current_site.domain,
            "user": data1,
            "data": data2,
            }
            email = render_to_string(email_template_name, context)
            try:
                msg = EmailMultiAlternatives(subject, email, settings.EMAIL_HOST_USER, [data1.email])
                msg.send()
            except BadHeaderError:
                return redirect('Invalid header found.')
            messages.success(request, 'Account Creation Successful.')
            return redirect(reverse('customerdetail', args=[data2.account_number]))
    return render(request, 'staff/createcustomer.html', {'unread_conversation':unread_conversation, 'form1':form1, 'form2':form2})

@staff_member_required(login_url='staff_login')
def CustomerDetailView(request, q):
    unread_conversation = Conversation.objects.annotate(
        unread_messages_count = Count('chat', filter=~Q(chat__sender=request.user) & Q(chat__read=False))
    ).filter(
        participants=request.user,
        unread_messages_count__gt=0
    ).count()
    try:
        account = CustomerAccount.objects.get(user__is_customer=True, account_number=q)
    except CustomerAccount.DoesNotExist:
        previous_url = request.META.get('HTTP_REFERER')
        if previous_url:
            messages.error(request, 'No Customer Account Found')
            return redirect(previous_url)
        else:
            return redirect('staff_home')
    
    def spent():
        try:
            txn = Txn.objects.filter(account=account, date__date=datetime.datetime.now().date())
        except Txn.DoesNotExist:
            txn = None
        trans = [float(tin.amount) for tin in txn]
        return sum(trans)
    def account_limit():
        return account.txn_limit
    txn_limit = account_limit() - spent()
    account.txn_limit_remaining = txn_limit
    
    if request.method == 'POST':
        form = PictureForm(request.POST, request.FILES)
        if form.is_valid():
            account.picture = form.cleaned_data['picture']
            account.save()
            messages.success(request, 'Picture Added Successfully')
            return redirect(reverse('customerdetail', args=[account.account_number]))
    else:
        form = PictureForm()
    return render(request, 'staff/customerprofile.html', {'unread_conversation':unread_conversation, 'account':account, 'form':form})

@staff_member_required(login_url='staff_login')
def EditCustomerView(request, pk):
    unread_conversation = Conversation.objects.annotate(
        unread_messages_count = Count('chat', filter=~Q(chat__sender=request.user) & Q(chat__read=False))
    ).filter(
        participants=request.user,
        unread_messages_count__gt=0
    ).count()
    account = CustomerAccount.objects.get(id=pk)
    if request.method == 'POST':
        if account.user.email_notification == False:
            account.user.email_notification = True
            account.user.save()
            messages.success(request, "User's Email Notification Is On")
            return redirect(reverse('editcustomer', args=[account.pk]))
        if account.user.email_notification == True:
            account.user.email_notification = False
            account.user.save()
            messages.success(request, "User's Email Notification Is Off")
            return redirect(reverse('editcustomer', args=[account.pk]))
    return render(request, 'staff/editcustomer.html', {'unread_conversation':unread_conversation, 'account':account})

@staff_member_required(login_url='staff_login')
def ModifyCustomerLimitView(request, pk):
    unread_conversation = Conversation.objects.annotate(
        unread_messages_count = Count('chat', filter=~Q(chat__sender=request.user) & Q(chat__read=False))
    ).filter(
        participants=request.user,
        unread_messages_count__gt=0
    ).count()
    account = CustomerAccount.objects.get(id=pk)
    if request.method == 'POST':
        if account.user.balance < float(1000):
            messages.error(request, 'Customer Has Insufficient Funds')
            return redirect(reverse('customerdetail', args=[account.account_number]))
        else:
            account.user.balance -= 1000
            account.user.save()
            account.bvn = request.POST['bvn']
            account.txn_limit = 1000000
            account.save()
            alert = Alert(amount=float(1000), balance=account.user.balance, user=account.user, modify_limit=True, txn='Debit', how='Mobile', which='Patridge Bank')
            alert.detail = f'Modify_Transfer_Limit/{alert.how}/{alert.which}'
            alert.save()
            message = Message(user=account.user, message=f'Patridge Bank: Congrats, Your Daily Transaction Limit Has Been Upgraded')
            message.save()
            if account.user.email_notification == True:
                subject = 'Patridge Bank: Daily Transaction Limit Upgraded'
                email_template_name = 'mail/limit_success.txt'
                current_site = get_current_site(request)
                context = {
                'domain': current_site.domain,
                "user": account.user,
                "account": account,
                'date': timezone.now().date()
                }
                email = render_to_string(email_template_name, context)
                try:
                    msg = EmailMultiAlternatives(subject, email, settings.EMAIL_HOST_USER , [account.user.email])
                    msg.send()
                except BadHeaderError:
                    return redirect('Invalid header found.')
            messages.success(request, "Customer's Daily Transaction Limit Has Been Upgraded")
            return redirect(reverse('editcustomer', args=[account.pk]))
    return render(request, 'staff/modifycustomerlimit.html', {'unread_conversation':unread_conversation, 'account':account})

@staff_member_required(login_url='staff_login')
def EditCustomerDetailView(request, pk):
    unread_conversation = Conversation.objects.annotate(
        unread_messages_count = Count('chat', filter=~Q(chat__sender=request.user) & Q(chat__read=False))
    ).filter(
        participants=request.user,
        unread_messages_count__gt=0
    ).count()
    account = CustomerAccount.objects.get(id=pk)
    if request.method == 'POST':
        form1 = UpdateUserForm(request.POST, instance=account.user)
        form2 = CustomerAccountCreationForm(request.POST, instance=account)
        if form1.is_valid() and form2.is_valid():
            form1.save()
            form2.save()
            messages.success(request, 'Profile Saved')
            return redirect(reverse('customerdetail', args=[account.account_number]))
    else:
        form1 = UpdateUserForm(instance=account.user)
        form2 = CustomerAccountCreationForm(instance=account)
    return render(request, 'staff/editcustomerdetail.html', {'unread_conversation':unread_conversation, 'form1':form1, 'form2':form2, 'account':account})

@staff_member_required(login_url='staff_login')
def ChangeCustomerPasswordView(request, pk):
    unread_conversation = Conversation.objects.annotate(
        unread_messages_count = Count('chat', filter=~Q(chat__sender=request.user) & Q(chat__read=False))
    ).filter(
        participants=request.user,
        unread_messages_count__gt=0
    ).count()
    account = CustomerAccount.objects.get(id=pk)
    user = account.user
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            user.set_password(form.cleaned_data['new_password1'])
            user.save()
            messages.success(request, 'New Password Has Been Set For User')
            return redirect(reverse('customerdetail', args=[account.account_number]))
    else:
        form = SetPasswordForm(user)
    return render(request, 'staff/customerpasswordchange.html', {'unread_conversation':unread_conversation, 'form':form, 'account':account})

@staff_member_required(login_url='staff_login')
def ChangeCustomerPinView(request, pk):
    unread_conversation = Conversation.objects.annotate(
        unread_messages_count = Count('chat', filter=~Q(chat__sender=request.user) & Q(chat__read=False))
    ).filter(
        participants=request.user,
        unread_messages_count__gt=0
    ).count()
    account = CustomerAccount.objects.get(id=pk)
    if request.method == 'POST':
        if request.POST['new_pin1'] == request.POST['new_pin2']:
            account.user.pin = request.POST['new_pin1']
            account.user.save()
            message = Message(user=account.user, message=f'Patridge Bank: Transaction Pin Changed Successfully')
            message.save()
            if account.user.email_notification == True:
                subject = 'Patridge Bank: Transaction Pin Change Success'
                email_template_name = 'mail/pin_change_success.txt'
                current_site = get_current_site(request)
                context = {
                'domain': current_site.domain,
                "user": account.user,
                "account": account,
                'date': timezone.now().date()
                }
                email = render_to_string(email_template_name, context)
                try:
                    msg = EmailMultiAlternatives(subject, email, settings.EMAIL_HOST_USER , [account.user.email])
                    msg.send()
                except BadHeaderError:
                    return redirect('Invalid header found.')
            messages.success(request, "User's Transaction Pin Has Been Changed")
            return redirect(reverse('customerdetail', args=[account.account_number]))
        else:
            messages.error(request, 'Pin Does Not Match')
            return redirect(reverse('changecustomerpin', args=[account.pk]))
    return render(request, 'staff/changecustomerpin.html', {'unread_conversation':unread_conversation, 'account':account})

@staff_member_required(login_url='staff_login')
def DeleteCustomerView(request):
    if request.method == 'POST':
        account_id = request.POST.get('account_id')
        account = CustomerAccount.objects.get(id=account_id)
        user = account.user
        account.delete()
        user.delete()
        return JsonResponse({'message': 'Account Deleted Successfully'})

@staff_member_required(login_url='staff_login')
def ChangeCustomerUserIDView(request, pk):
    unread_conversation = Conversation.objects.annotate(
        unread_messages_count = Count('chat', filter=~Q(chat__sender=request.user) & Q(chat__read=False))
    ).filter(
        participants=request.user,
        unread_messages_count__gt=0
    ).count()
    account = CustomerAccount.objects.get(id=pk)
    if request.method == 'POST':
        if len(request.POST['new_user_id']) > 11 or len(request.POST['new_user_id']) < 11:
            messages.error(request, 'Length Of User ID Should Be 11 Digits')
            return redirect(reverse('changecustomeruserid', args=[account.pk]))
        else:
            account.user.user_ID = request.POST['new_user_id']
            account.user.save()
            message = Message(user=account.user, message=f'Patridge Bank: User ID Changed Successfully')
            message.save()
            if account.user.email_notification == True:
                subject = 'Patridge Bank: User ID Change Success'
                email_template_name = 'mail/user_id_success.txt'
                current_site = get_current_site(request)
                context = {
                'domain': current_site.domain,
                "user": account.user,
                "account": account,
                'date': timezone.now().date()
                }
                email = render_to_string(email_template_name, context)
                try:
                    msg = EmailMultiAlternatives(subject, email, settings.EMAIL_HOST_USER , [account.user.email])
                    msg.send()
                except BadHeaderError:
                    return redirect('Invalid header found.')
            messages.success(request, 'User ID Changed Successfully')
            return redirect(reverse('customerdetail', args=[account.account_number]))
    return render(request, 'staff/changecustomeruserid.html', {'unread_conversation':unread_conversation, 'account':account})

@staff_member_required(login_url='staff_login')
def TransactionHistoryView(request, pk):
    unread_conversation = Conversation.objects.annotate(
        unread_messages_count = Count('chat', filter=~Q(chat__sender=request.user) & Q(chat__read=False))
    ).filter(
        participants=request.user,
        unread_messages_count__gt=0
    ).count()
    account = CustomerAccount.objects.get(id=pk)
    txn = Alert.objects.filter(user=account.user).exclude(transfer__status='Processing', bill__status='Processing', topup__status='Processing').order_by('-date')
    paginator = Paginator(txn, 20)
    page = request.GET.get('page')
    try:
        txn = paginator.page(page)
    except PageNotAnInteger:
        txn = paginator.page(1)
    except EmptyPage:
        txn = paginator.page(paginator.num_pages)
    return render(request, 'staff/txnhistory.html', {'unread_conversation':unread_conversation, 'account':account, 'txn':txn, 'fulltxn':'fulltxn'})

@staff_member_required(login_url='staff_login')
def TransactionDetailView(request, pk, id):
    unread_conversation = Conversation.objects.annotate(
        unread_messages_count = Count('chat', filter=~Q(chat__sender=request.user) & Q(chat__read=False))
    ).filter(
        participants=request.user,
        unread_messages_count__gt=0
    ).count()
    txn = Alert.objects.get(id=pk)
    account = CustomerAccount.objects.get(id=id)
    context = {
        'unread_conversation':unread_conversation,
        'txn':txn,
        'account':account        
    }
    return render(request, 'staff/txndetail.html', context)

@staff_member_required(login_url='staff_login')
def DebitFilterView(request, pk):
    unread_conversation = Conversation.objects.annotate(
        unread_messages_count = Count('chat', filter=~Q(chat__sender=request.user) & Q(chat__read=False))
    ).filter(
        participants=request.user,
        unread_messages_count__gt=0
    ).count()
    account = CustomerAccount.objects.get(id=pk)
    txn = Alert.objects.filter(user=account.user, txn='Debit').exclude(transfer__status='Processing', bill__status='Processing', topup__status='Processing').order_by('-date')
    paginator = Paginator(txn, 20)
    page = request.GET.get('page')
    try:
        txn = paginator.page(page)
    except PageNotAnInteger:
        txn = paginator.page(1)
    except EmptyPage:
        txn = paginator.page(paginator.num_pages)
    return render(request, 'staff/txnhistory.html', {'unread_conversation':unread_conversation, 'account':account, 'txn':txn, 'debit':'debit'})

@staff_member_required(login_url='staff_login')
def CreditFilterView(request, pk):
    unread_conversation = Conversation.objects.annotate(
        unread_messages_count = Count('chat', filter=~Q(chat__sender=request.user) & Q(chat__read=False))
    ).filter(
        participants=request.user,
        unread_messages_count__gt=0
    ).count()
    account = CustomerAccount.objects.get(id=pk)
    txn = Alert.objects.filter(user=account.user, txn='Credit').exclude(transfer__status='Processing', bill__status='Processing', topup__status='Processing').order_by('-date')
    paginator = Paginator(txn, 20)
    page = request.GET.get('page')
    try:
        txn = paginator.page(page)
    except PageNotAnInteger:
        txn = paginator.page(1)
    except EmptyPage:
        txn = paginator.page(paginator.num_pages)
    return render(request, 'staff/txnhistory.html', {'unread_conversation':unread_conversation, 'account':account, 'txn':txn, 'credit':'credit'})

@staff_member_required(login_url='staff_login')
def TransferFilterView(request, pk):
    unread_conversation = Conversation.objects.annotate(
        unread_messages_count = Count('chat', filter=~Q(chat__sender=request.user) & Q(chat__read=False))
    ).filter(
        participants=request.user,
        unread_messages_count__gt=0
    ).count()
    account = CustomerAccount.objects.get(id=pk)
    txn = Alert.objects.filter(user=account.user, transfer__user=account.user, transfer__status='Completed').order_by('-date')
    paginator = Paginator(txn, 20)
    page = request.GET.get('page')
    try:
        txn = paginator.page(page)
    except PageNotAnInteger:
        txn = paginator.page(1)
    except EmptyPage:
        txn = paginator.page(paginator.num_pages)
    return render(request, 'staff/txnhistory.html', {'unread_conversation':unread_conversation, 'account':account, 'txn':txn, 'transfer':'transfer'})

@staff_member_required(login_url='staff_login')
def BillFilterView(request, pk):
    unread_conversation = Conversation.objects.annotate(
        unread_messages_count = Count('chat', filter=~Q(chat__sender=request.user) & Q(chat__read=False))
    ).filter(
        participants=request.user,
        unread_messages_count__gt=0
    ).count()
    account = CustomerAccount.objects.get(id=pk)
    txn = Alert.objects.filter(user=account.user, bill__account=account, bill__status='Completed').order_by('-date')
    paginator = Paginator(txn, 20)
    page = request.GET.get('page')
    try:
        txn = paginator.page(page)
    except PageNotAnInteger:
        txn = paginator.page(1)
    except EmptyPage:
        txn = paginator.page(paginator.num_pages)
    return render(request, 'staff/txnhistory.html', {'unread_conversation':unread_conversation, 'account':account, 'txn':txn, 'bill':'bill'})

@staff_member_required(login_url='staff_login')
def TopUpFilterView(request, pk):
    unread_conversation = Conversation.objects.annotate(
        unread_messages_count = Count('chat', filter=~Q(chat__sender=request.user) & Q(chat__read=False))
    ).filter(
        participants=request.user,
        unread_messages_count__gt=0
    ).count()
    account = CustomerAccount.objects.get(id=pk)
    txn = Alert.objects.filter(user=account.user, topup__account=account, topup__status='Completed').order_by('-date')
    paginator = Paginator(txn, 20)
    page = request.GET.get('page')
    try:
        txn = paginator.page(page)
    except PageNotAnInteger:
        txn = paginator.page(1)
    except EmptyPage:
        txn = paginator.page(paginator.num_pages)
    return render(request, 'staff/txnhistory.html', {'unread_conversation':unread_conversation, 'account':account, 'txn':txn, 'topup':'topup'})

@staff_member_required(login_url='staff_login')
def LoanFilterView(request, pk):
    unread_conversation = Conversation.objects.annotate(
        unread_messages_count = Count('chat', filter=~Q(chat__sender=request.user) & Q(chat__read=False))
    ).filter(
        participants=request.user,
        unread_messages_count__gt=0
    ).count()
    account = CustomerAccount.objects.get(id=pk)
    txn = Alert.objects.filter(user=account.user, loan__account=account).order_by('-date')
    paginator = Paginator(txn, 20)
    page = request.GET.get('page')
    try:
        txn = paginator.page(page)
    except PageNotAnInteger:
        txn = paginator.page(1)
    except EmptyPage:
        txn = paginator.page(paginator.num_pages)
    return render(request, 'staff/txnhistory.html', {'unread_conversation':unread_conversation, 'account':account, 'txn':txn, 'loan':'loan'})

@staff_member_required(login_url='staff_login')
def DateFilterView(request, start, stop, pk):
    unread_conversation = Conversation.objects.annotate(
        unread_messages_count = Count('chat', filter=~Q(chat__sender=request.user) & Q(chat__read=False))
    ).filter(
        participants=request.user,
        unread_messages_count__gt=0
    ).count()
    account = CustomerAccount.objects.get(id=pk)
    try:
        txn = Alert.objects.filter(user=account.user, date__date__range=(start, stop)).exclude(transfer__status='Processing', bill__status='Processing', topup__status='Processing').order_by('-date')
        paginator = Paginator(txn, 20)
        page = request.GET.get('page')
        try:
            txn = paginator.page(page)
        except PageNotAnInteger:
            txn = paginator.page(1)
        except EmptyPage:
            txn = paginator.page(paginator.num_pages)
    except(Alert.DoesNotExist):
        txn = None
    return render(request, 'staff/txnhistory.html', {'unread_conversation':unread_conversation, 'account':account, 'txn':txn, 'date':'date', 'start':start, 'stop':stop})

@staff_member_required(login_url='staff_login')
def AmountFilterView(request, start, stop, pk):
    unread_conversation = Conversation.objects.annotate(
        unread_messages_count = Count('chat', filter=~Q(chat__sender=request.user) & Q(chat__read=False))
    ).filter(
        participants=request.user,
        unread_messages_count__gt=0
    ).count()
    account = CustomerAccount.objects.get(id=pk)
    try:
        txn = Alert.objects.filter(user=account.user, amount__range=(start, stop)).exclude(transfer__status='Processing', bill__status='Processing', topup__status='Processing').order_by('-date')
        paginator = Paginator(txn, 20)
        page = request.GET.get('page')
        try:
            txn = paginator.page(page)
        except PageNotAnInteger:
            txn = paginator.page(1)
        except EmptyPage:
            txn = paginator.page(paginator.num_pages)
    except(Alert.DoesNotExist):
        txn = None
    return render(request, 'staff/txnhistory.html', {'unread_conversation':unread_conversation, 'account':account, 'txn':txn, 'amount':'amount', 'start':start, 'stop':stop})

@staff_member_required(login_url='staff_login')
def CardManagementView(request, pk):
    unread_conversation = Conversation.objects.annotate(
        unread_messages_count = Count('chat', filter=~Q(chat__sender=request.user) & Q(chat__read=False))
    ).filter(
        participants=request.user,
        unread_messages_count__gt=0
    ).count()
    account = CustomerAccount.objects.get(id=pk)
    try:
        card = Card.objects.get(account=account, expires__gt=datetime.datetime.now().date())
    except(Card.DoesNotExist):
        card = None
    return render(request, 'staff/customercard.html', {'unread_conversation':unread_conversation, 'card':card, 'account':account})

@staff_member_required(login_url='staff_login')
def ChangeCustomerCardPin(request, pk):
    unread_conversation = Conversation.objects.annotate(
        unread_messages_count = Count('chat', filter=~Q(chat__sender=request.user) & Q(chat__read=False))
    ).filter(
        participants=request.user,
        unread_messages_count__gt=0
    ).count()
    card = Card.objects.get(id=pk)
    if request.method == 'POST':
        if request.POST['new_pin1'] == request.POST['new_pin2']:
            card.pin = request.POST['new_pin1']
            card.save()
            message = Message(user=card.account.user, message=f'Patridge Bank: Card Pin Changed Successfully')
            message.save()
            messages.success(request, "User's Card Pin Has Been Changed")
            return redirect(reverse('cardmanage', args=[card.account.pk]))
        else:
            messages.error(request, 'Pin Does Not Match')
            return redirect(reverse('changecustomercardpin', args=[card.pk]))
    return render(request, 'staff/changecustomercardpin.html', {'unread_conversation':unread_conversation, 'card':card})

@staff_member_required(login_url='staff_login')
def DeleteCardView(request):
    if request.method == 'POST':
        card_id = request.POST.get('card_id')
        card = Card.objects.get(id=card_id)
        card.delete()
        return JsonResponse({'message': 'Card Removed Successfully'})

@staff_member_required(login_url='staff_login')
def RequestCustomerCardView(request, pk):
    unread_conversation = Conversation.objects.annotate(
        unread_messages_count = Count('chat', filter=~Q(chat__sender=request.user) & Q(chat__read=False))
    ).filter(
        participants=request.user,
        unread_messages_count__gt=0
    ).count()
    account = CustomerAccount.objects.get(id=pk)
    try:
        card = Card.objects.get(account=account, expires__gt=datetime.datetime.now().date())
    except(Card.DoesNotExist):
        card = None
    if request.method == 'POST':
        if account.user.balance < float(1000):
            messages.error(request, 'User Has Insufficient Balance')
            return redirect(reverse('cardmanage', args=[account.pk]))
        else:
            if request.POST['pin1'] == request.POST['pin2']:
                if Card.objects.filter(account=account, expires__gt=datetime.datetime.now().date()).exists():
                    old = Card.objects.get(account=account, expires__gt=datetime.datetime.now().date())
                    old.delete()
                account.user.balance -= float(1000)
                account.user.save()
                new = Card(account=account, card_id=generate_card_id(), card_number=generate_card_number(), cvv=generate_cvv(), expires=expires(), card_type='VISA', card='Debit', pin=request.POST['pin1'])
                try:
                    new.save()
                except(ValueError):
                    messages.error(request, 'Pin Should Be Digits')
                    return redirect(reverse('requestcard', args=[account.pk]))
                alert = Alert(amount=float(1000), balance=account.user.balance, user=account.user, card=new, txn='Debit', how='Card', which='Patridge Bank')
                alert.detail = f'{alert.card.card_id}/{alert.which}/{alert.how} Payment'
                alert.save()
                txn = Txn(account=account, amount=float(1000))
                txn.save()
                message = Message(user=account.user, message=f'Patridge Bank: Congrats, You Have Gotten A Patridge Bank Virtual Card')
                message.save()
                if account.user.email_notification == True:
                    subject = 'Patridge Bank: Virtual Card Request Successful'
                    email_template_name = 'mail/card_success.txt'
                    current_site = get_current_site(request)
                    context = {
                    'domain': current_site.domain,
                    "user": account.user,
                    "card": new,
                    }
                    email = render_to_string(email_template_name, context)
                    try:
                        msg = EmailMultiAlternatives(subject, email, settings.EMAIL_HOST_USER , [account.user.email])
                        msg.send()
                    except BadHeaderError:
                        return redirect('Invalid header found.')
                messages.success(request, 'Congrats, Patridge Bank Virtual Card Has Been Created Successfully')
                return redirect(reverse('cardmanage', args=[account.pk]))
            else:
                messages.error(request, 'Card Pin Not Thesame')
                return redirect(reverse('requestcard', args=[account.pk]))
    return render(request, 'staff/requestcustomercard.html', {'unread_conversation':unread_conversation, 'account':account, 'card':card})

@staff_member_required(login_url='staff_login')
def LoanManagementView(request, pk):
    unread_conversation = Conversation.objects.annotate(
        unread_messages_count = Count('chat', filter=~Q(chat__sender=request.user) & Q(chat__read=False))
    ).filter(
        participants=request.user,
        unread_messages_count__gt=0
    ).count()
    account = CustomerAccount.objects.get(id=pk)
    all_loan = Loan.objects.filter(account=account).order_by('-date')
    try:
        requested = Loan.objects.filter(account=account, approved=False, disapproved=False)
    except(Loan.DoesNotExist):
        requested = None
    try:
        valid_loan = Loan.objects.get(account=account, approved=True, paid=False, till__gte=timezone.now().date())
        interest = (0.5/100) * valid_loan.amount
        if timezone.now().date() - valid_loan.date.date():
            day = timezone.now().date() - valid_loan.date.date()
            days = day.days
        else:
            days = 0
        total_interest = float(interest) * float(days)
        valid_loan.new_amount = valid_loan.amount + total_interest
        valid_loan.save()
    except(Loan.DoesNotExist):
        valid_loan = None
    try:
        in_debt_object = Loan.objects.get(account=account, approved=True, paid=False, till__lt=timezone.now().date())
        interest = (0.5/100) * in_debt_object.amount
        if timezone.now().date() - in_debt_object.date.date():
            day = timezone.now().date() - in_debt_object.date.date()
            days = day.days
        else:
            days = 0
        total_interest = float(interest) * float(days)
        in_debt_object.new_amount = in_debt_object.amount + total_interest
        in_debt_object.save()
    except(Loan.DoesNotExist):
        in_debt_object = None
    return render(request, 'staff/customerloan.html', {'unread_conversation':unread_conversation, 'loan':'loan', 'all_loan':all_loan, 'account':account, 'requested':requested, 'valid_loan':valid_loan, 'in_debt_object':in_debt_object})

@staff_member_required(login_url='staff_login')
def LoanManagementDetailView(request, pk):
    unread_conversation = Conversation.objects.annotate(
        unread_messages_count = Count('chat', filter=~Q(chat__sender=request.user) & Q(chat__read=False))
    ).filter(
        participants=request.user,
        unread_messages_count__gt=0
    ).count()
    loan = Loan.objects.get(id=pk)
    context = {
        'unread_conversation':unread_conversation,
        'loan':loan
    }
    return render(request, 'staff/loanmanagementdetail.html', context)

@staff_member_required(login_url='staff_login')
def RequestCustomerLoanView(request, pk):
    unread_conversation = Conversation.objects.annotate(
        unread_messages_count = Count('chat', filter=~Q(chat__sender=request.user) & Q(chat__read=False))
    ).filter(
        participants=request.user,
        unread_messages_count__gt=0
    ).count()
    account = CustomerAccount.objects.get(id=pk)
    if request.method == 'POST':
        if not Loan.objects.filter(account=account, approved=True, paid=False).exists():
            if date_eligible(account=account).date() < timezone.now().date() and transaction_eligible(account=account) > float(10000):
                if request.POST['date'] < str(timezone.now().date()):
                    messages.error(request, 'Date Should Be Beyond Today')
                    return redirect(reverse('requestloan', args=[account.pk]))
                else:
                    if '1week' in request.POST and not '1month' in request.POST and not '3months' in request.POST and not '6months' in request.POST:
                        new = Loan(account=account, reason=request.POST['reason'], amount=float(request.POST['amount']), new_amount=float(request.POST['amount']), source_of_income=request.POST['income'], till=request.POST['date'], period='1 Week')
                        new.save()
                        account.user.balance += new.amount
                        account.user.save()
                        message = Message(user=account.user, message=f'Patridge Bank: Loan Request Of {new.amount} Is Successful')
                        message.save()
                        alert = Alert(amount=new.amount, balance=account.user.balance, user=account.user, loan=new, txn='Credit', how='Mobile', which='Patridge Bank')
                        alert.detail = f'Loan/{alert.how}/{alert.which}'
                        alert.save()
                        new.approved = True
                        new.save()
                        if account.user.email_notification == True:
                            subject = 'Patridge Bank: Loan Request Successful'
                            email_template_name = 'mail/loan_request_success.txt'
                            current_site = get_current_site(request)
                            context = {
                            'domain': current_site.domain,
                            "user": account.user,
                            'new':new,
                            "account": account,
                            'date': timezone.now().date()
                            }
                            email = render_to_string(email_template_name, context)
                            try:
                                msg = EmailMultiAlternatives(subject, email, settings.EMAIL_HOST_USER , [account.user.email])
                                msg.send()
                            except BadHeaderError:
                                return redirect('Invalid header found.')
                        messages.success(request, 'Loan Request Successful')
                        return redirect(reverse('loanmanage', args=[account.pk]))
                    elif not '1week' in request.POST and '1month' in request.POST and not '3months' in request.POST and not '6months' in request.POST:
                        new = Loan(account=account, reason=request.POST['reason'], amount=float(request.POST['amount']), new_amount=float(request.POST['amount']), source_of_income=request.POST['income'], till=request.POST['date'], period='1 Month')
                        new.save()
                        account.user.balance += new.amount
                        account.user.save()
                        message = Message(user=account.user, message=f'Patridge Bank: Loan Request Of {new.amount} Is Successful')
                        message.save()
                        alert = Alert(amount=new.amount, balance=account.user.balance, user=account.user, loan=new, txn='Credit', how='Mobile', which='Patridge Bank')
                        alert.detail = f'Loan/{alert.how}/{alert.which}'
                        alert.save()
                        new.approved = True
                        new.save()
                        if account.user.email_notification == True:
                            subject = 'Patridge Bank: Loan Request Successful'
                            email_template_name = 'mail/loan_request_success.txt'
                            current_site = get_current_site(request)
                            context = {
                            'domain': current_site.domain,
                            "user": account.user,
                            'new':new,
                            "account": account,
                            'date': timezone.now().date()
                            }
                            email = render_to_string(email_template_name, context)
                            try:
                                msg = EmailMultiAlternatives(subject, email, settings.EMAIL_HOST_USER , [account.user.email])
                                msg.send()
                            except BadHeaderError:
                                return redirect('Invalid header found.')
                        messages.success(request, 'Loan Request Successful')
                        return redirect(reverse('loanmanage', args=[account.pk]))
                    elif not '1week' in request.POST and not '1month' in request.POST and '3months' in request.POST and not '6months' in request.POST:
                        new = Loan(account=account, reason=request.POST['reason'], amount=float(request.POST['amount']), new_amount=float(request.POST['amount']), source_of_income=request.POST['income'], till=request.POST['date'], period='3 Months')
                        new.save()
                        account.user.balance += new.amount
                        account.user.save()
                        message = Message(user=account.user, message=f'Patridge Bank: Loan Request Of {new.amount} Is Successful')
                        message.save()
                        alert = Alert(amount=new.amount, balance=account.user.balance, user=account.user, loan=new, txn='Credit', how='Mobile', which='Patridge Bank')
                        alert.detail = f'Loan/{alert.how}/{alert.which}'
                        alert.save()
                        new.approved = True
                        new.save()
                        if account.user.email_notification == True:
                            subject = 'Patridge Bank: Loan Request Successful'
                            email_template_name = 'mail/loan_request_success.txt'
                            current_site = get_current_site(request)
                            context = {
                            'domain': current_site.domain,
                            "user": account.user,
                            'new':new,
                            "account": account,
                            'date': timezone.now().date()
                            }
                            email = render_to_string(email_template_name, context)
                            try:
                                msg = EmailMultiAlternatives(subject, email, settings.EMAIL_HOST_USER , [account.user.email])
                                msg.send()
                            except BadHeaderError:
                                return redirect('Invalid header found.')
                        messages.success(request, 'Loan Request Successful')
                        return redirect(reverse('loanmanage', args=[account.pk]))
                    elif not '1week' in request.POST and not '1month' in request.POST and not '3months' in request.POST and '6months' in request.POST:
                        new = Loan(account=account, reason=request.POST['reason'], amount=float(request.POST['amount']), new_amount=float(request.POST['amount']), source_of_income=request.POST['income'], till=request.POST['date'], period='6 Months')
                        new.save()
                        account.user.balance += new.amount
                        account.user.save()
                        message = Message(user=account.user, message=f'Patridge Bank: Loan Request Of {new.amount} Is Successful')
                        message.save()
                        alert = Alert(amount=new.amount, balance=account.user.balance, user=account.user, loan=new, txn='Credit', how='Mobile', which='Patridge Bank')
                        alert.detail = f'Loan/{alert.how}/{alert.which}'
                        alert.save()
                        new.approved = True
                        new.save()
                        if account.user.email_notification == True:
                            subject = 'Patridge Bank: Loan Request Successful'
                            email_template_name = 'mail/loan_request_success.txt'
                            current_site = get_current_site(request)
                            context = {
                            'domain': current_site.domain,
                            "user": account.user,
                            'new':new,
                            "account": account,
                            'date': timezone.now().date()
                            }
                            email = render_to_string(email_template_name, context)
                            try:
                                msg = EmailMultiAlternatives(subject, email, settings.EMAIL_HOST_USER , [account.user.email])
                                msg.send()
                            except BadHeaderError:
                                return redirect('Invalid header found.')
                        messages.success(request, 'Loan Request Successful')
                        return redirect(reverse('loanmanage', args=[account.pk]))
                    else:
                        messages.error(request, 'Invalid Choice In Loan Duration')
                        return redirect(reverse('requestloan', args=[account.pk]))
            else:
                messages.error(request, 'This Account Is Not Eligible For A Loan With Us')
                return redirect(reverse('loanmanage', args=[account.pk]))
        else:
            messages.error(request, 'This User Has An Outstanding Loan')
            return redirect(reverse('loanmanage', args=[account.pk]))
    return render(request, 'staff/requestcustomerloan.html', {'unread_conversation':unread_conversation, 'account':account})

@staff_member_required(login_url='staff_login')
def DisapproveCustomerLoanView(request):
    if request.method == 'POST':
        loan_id = request.POST.get('loan_id')
        loan = Loan.objects.get(id=loan_id)
        loan.disapproved = True
        loan.save()
        return JsonResponse({'message': "Loan Has Been Disapproved"})

@staff_member_required(login_url='staff_login')
def ApproveCustomerLoanView(request, date, loan_id):
    loan = Loan.objects.get(id=loan_id)
    account = loan.account
    if not Loan.objects.filter(account=account, approved=True, paid=False).exists():
        if date < str(timezone.now().date()):
            messages.error(request, 'Date Should Be Beyond Today')
            return redirect(reverse('loanmanagedetail', args=[loan.pk]))
        else:
            account.user.balance += loan.amount
            account.user.save()
            message = Message(user=account.user, message=f'Patridge Bank: Loan Request Of {loan.amount} Has Been Approved And Your Account Has Been Credited')
            message.save()
            alert = Alert(amount=loan.amount, balance=account.user.balance, user=account.user, loan=loan, txn='Credit', how='Mobile', which='Patridge Bank')
            alert.detail = f'Loan/{alert.how}/{alert.which}'
            alert.save()
            loan.till = date
            loan.approved = True
            loan.save()
            if account.user.email_notification == True:
                subject = 'Patridge Bank: Loan Request Approved'
                email_template_name = 'mail/loan_request_approved.txt'
                current_site = get_current_site(request)
                context = {
                'domain': current_site.domain,
                "user": account.user,
                'new':loan,
                "account": account,
                'date': timezone.now().date()
                }
                email = render_to_string(email_template_name, context)
                try:
                    msg = EmailMultiAlternatives(subject, email, settings.EMAIL_HOST_USER , [account.user.email])
                    msg.send()
                except BadHeaderError:
                    return redirect('Invalid header found.')
            messages.success(request, 'Loan Has Been Approved')
            return redirect(reverse('loanmanage', args=[account.pk]))
    else:
        messages.error(request, 'This User Has An Outstanding Loan.')
        return redirect(reverse('loanmanage', args=[account.pk]))

@staff_member_required(login_url='staff_login')
def PayCustomerLoanView(request, pk):
    loan = Loan.objects.get(id=pk)
    account = loan.account
    if account.user.balance > loan.new_amount or account.user.balance == loan.new_amount:
        account.user.balance -= loan.new_amount
        account.user.save()
        loan.paid = True
        loan.save()
        message = Message(user=account.user, message=f'Patridge Bank: Loan Payment Successful')
        message.save()
        alert = Alert(amount=loan.new_amount, balance=account.user.balance, user=account.user, loan=loan, txn='Debit', how='Mobile', which='Patridge Bank')
        alert.detail = f'Loan_Payment/{alert.how}/{alert.which}'
        alert.save()
        if account.user.email_notification == True:
            subject = 'Patridge Bank: Loan Payment Successful'
            email_template_name = 'mail/loan_repay_success.txt'
            current_site = get_current_site(request)
            context = {
            'domain': current_site.domain,
            "user": account.user,
            'loan':loan,
            "account": account,
            'date': timezone.now().date()
            }
            email = render_to_string(email_template_name, context)
            try:
                msg = EmailMultiAlternatives(subject, email, settings.EMAIL_HOST_USER , [account.user.email])
                msg.send()
            except BadHeaderError:
                return redirect('Invalid header found.')
        messages.success(request, 'User Loan Has Been Paid')
        return redirect(reverse('loanmanage', args=[account.pk]))
    else:
        messages.error(request, 'User Has Insufficient Funds')
        return redirect(reverse('loanmanage', args=[account.pk]))

@staff_member_required(login_url='staff_login')
def SCalculatorView(request):
    unread_conversation = Conversation.objects.annotate(
        unread_messages_count = Count('chat', filter=~Q(chat__sender=request.user) & Q(chat__read=False))
    ).filter(
        participants=request.user,
        unread_messages_count__gt=0
    ).count()
    if request.method == 'POST':
        if 'principal' in request.POST and 'time' in request.POST:
            principal = float(request.POST['principal'])
            time = float(request.POST['time'])
            interest = ((0.5/100) * principal) * time
            total = float(interest) + float(request.POST['principal'])
            context = {
                'result':'result',
                'principal':principal,
                'time':time,
                'interest':interest,
                'total':total
                }
            return render(request, 'staff/interestcalculator.html', context)
        else:
            messages.error(request, 'Invalid Input')
            return redirect('scalculate')
    return render(request, 'staff/interestcalculator.html', {'unread_conversation':unread_conversation})

@staff_member_required(login_url='staff_login')
def GeneralLoanManagementView(request):
    unread_conversation = Conversation.objects.annotate(
        unread_messages_count = Count('chat', filter=~Q(chat__sender=request.user) & Q(chat__read=False))
    ).filter(
        participants=request.user,
        unread_messages_count__gt=0
    ).count()
    return render(request, 'staff/loanmenu.html', {'unread_conversation':unread_conversation})

@staff_member_required(login_url='staff_login')
def AllLoanView(request):
    unread_conversation = Conversation.objects.annotate(
        unread_messages_count = Count('chat', filter=~Q(chat__sender=request.user) & Q(chat__read=False))
    ).filter(
        participants=request.user,
        unread_messages_count__gt=0
    ).count()
    if 'q' in request.POST:
        q = request.POST['q']
        all_loan = Loan.objects.filter(account__account_number=q).order_by('-date')
    else:
        all_loan = Loan.objects.order_by('-date')
    for loan in all_loan:
        if loan.approved == True and loan.paid == False and loan.till > timezone.now().date():
            interest = (0.5/100) * loan.amount
            if timezone.now().date() - loan.date.date():
                day = timezone.now().date() - loan.date.date()
                days = day.days
            else:
                days = 0
            total_interest = float(interest) * float(days)
            loan.new_amount = loan.amount + total_interest
            loan.save()
        if loan.approved == True and loan.paid == False and loan.till < timezone.now().date():
            interest = (0.5/100) * loan.amount
            if timezone.now().date() - loan.date.date():
                day = timezone.now().date() - loan.date.date()
                days = day.days
            else:
                days = 0
            total_interest = float(interest) * float(days)
            loan.new_amount = loan.amount + total_interest
            loan.save()
    paginator = Paginator(all_loan, 20)
    page = request.GET.get('page')
    try:
        all_loan = paginator.page(page)
    except PageNotAnInteger:
        all_loan = paginator.page(1)
    except EmptyPage:
        all_loan = paginator.page(paginator.num_pages)
    return render(request, 'staff/loanmanagement.html', {'unread_conversation':unread_conversation, 'all_loan':all_loan, 'allloan':'allloan'})

@staff_member_required(login_url='staff_login')
def RequestedLoanView(request):
    unread_conversation = Conversation.objects.annotate(
        unread_messages_count = Count('chat', filter=~Q(chat__sender=request.user) & Q(chat__read=False))
    ).filter(
        participants=request.user,
        unread_messages_count__gt=0
    ).count()
    if 'q' in request.POST:
        q = request.POST['q']
        requested = Loan.objects.filter(account__account_number=q, approved=False, disapproved=False).order_by('-date')
    else:
        requested = Loan.objects.filter(approved=False, disapproved=False).order_by('-date')
    paginator = Paginator(requested, 20)
    page = request.GET.get('page')
    try:
        requested = paginator.page(page)
    except PageNotAnInteger:
        requested = paginator.page(1)
    except EmptyPage:
        requested = paginator.page(paginator.num_pages)
    return render(request, 'staff/loanmanagement.html', {'unread_conversation':unread_conversation, 'requested':requested, 'allrequested':'allrequested'})

@staff_member_required(login_url='staff_login')
def ValidLoanView(request):
    unread_conversation = Conversation.objects.annotate(
        unread_messages_count = Count('chat', filter=~Q(chat__sender=request.user) & Q(chat__read=False))
    ).filter(
        participants=request.user,
        unread_messages_count__gt=0
    ).count()
    if 'q' in request.POST:
        q = request.POST['q']
        valid_loan_object = Loan.objects.filter(account__account_number=q, approved=True, paid=False, till__gte=timezone.now().date()).order_by('-date')
    else:
        valid_loan_object = Loan.objects.filter(approved=True, paid=False, till__gte=timezone.now().date()).order_by('-date')
    for valid_loan in valid_loan_object:
        interest = (0.5/100) * valid_loan.amount
        if timezone.now().date() - valid_loan.date.date():
            day = timezone.now().date() - valid_loan.date.date()
            days = day.days
        else:
            days = 0
        total_interest = float(interest) * float(days)
        valid_loan.new_amount = valid_loan.amount + total_interest
        valid_loan.save()
    paginator = Paginator(valid_loan_object, 20)
    page = request.GET.get('page')
    try:
        valid_loan_object = paginator.page(page)
    except PageNotAnInteger:
        valid_loan_object = paginator.page(1)
    except EmptyPage:
        valid_loan_object = paginator.page(paginator.num_pages)
    return render(request, 'staff/loanmanagement.html', {'unread_conversation':unread_conversation, 'valid_loan_object':valid_loan_object, 'valid_loan':'valid_loan'})
    
@staff_member_required(login_url='staff_login')
def InDebtLoanView(request):
    unread_conversation = Conversation.objects.annotate(
        unread_messages_count = Count('chat', filter=~Q(chat__sender=request.user) & Q(chat__read=False))
    ).filter(
        participants=request.user,
        unread_messages_count__gt=0
    ).count()
    if 'q' in request.POST:
        q = request.POST['q']
        in_debt_object = Loan.objects.filter(account__account_number=q, approved=True, paid=False, till__lt=timezone.now().date()).order_by('-date')
    else:
        in_debt_object = Loan.objects.filter(approved=True, paid=False, till__lt=timezone.now().date()).order_by('-date')
    for in_debt in in_debt_object:
        interest = (0.5/100) * in_debt.amount
        if timezone.now().date() - in_debt.date.date():
            day = timezone.now().date() - in_debt.date.date()
            days = day.days
        else:
            days = 0
        total_interest = float(interest) * float(days)
        in_debt.new_amount = in_debt.amount + total_interest
        in_debt.save()
    paginator = Paginator(in_debt_object, 20)
    page = request.GET.get('page')
    try:
        in_debt_object = paginator.page(page)
    except PageNotAnInteger:
        in_debt_object = paginator.page(1)
    except EmptyPage:
        in_debt_object = paginator.page(paginator.num_pages)
    return render(request, 'staff/loanmanagement.html', {'unread_conversation':unread_conversation, 'in_debt_object':in_debt_object, 'in_debt':'in_debt'})

@staff_member_required(login_url='staff_login')
def FreezeCustomerAccountView(request):
    if request.method == 'POST':
        account_id = request.POST.get('account_id')
        account = CustomerAccount.objects.get(id=account_id)
        user = account.user
        user.is_active = False
        user.save()
        return JsonResponse({'message': "Customer's Account Has Been Frozen"})

@staff_member_required(login_url='staff_login')
def UnFreezeCustomerAccountView(request):
    if request.method == 'POST':
        account_id = request.POST.get('account_id')
        account = CustomerAccount.objects.get(id=account_id)
        user = account.user
        user.is_active = True
        user.save()
        return JsonResponse({'message': "Customer's Account Has Been Unfrozen"})

@staff_member_required(login_url='staff_login')
def DrCrAccountView(request, customer_id):
    account = CustomerAccount.objects.get(id=customer_id)
    context = {
        'customer_name': f'{account.account_name} / {account.account_number}',
        'account_balance': account.user.balance,
    }
    return JsonResponse(context)

@staff_member_required(login_url='staff_login')
def CreditAccountView(request, customer_id, amount):
    account = CustomerAccount.objects.get(id=customer_id)
    account.user.balance += float(amount)
    account.user.save()
    alert = Alert(amount=float(amount), balance=account.user.balance, user=account.user, txn='Credit', how='Mobile', which='Patridge Bank')
    alert.detail = f'InBankCredit/{alert.how}/{alert.which}'
    alert.save()
    return JsonResponse({'message': 'Customer Credited Successfully'})

@staff_member_required(login_url='staff_login')
def DebitAccountView(request, customer_id, amount):
    account = CustomerAccount.objects.get(id=customer_id)
    if account.user.balance < float(amount):
        return JsonResponse({'message': 'Customer Has Insufficient Funds'})
    else:
        account.user.balance -= float(amount)
        account.user.save()
        alert = Alert(amount=amount, balance=account.user.balance, user=account.user, txn='Debit', how='Mobile', which='Patridge Bank')
        alert.detail = f'InBankDebit/{alert.how}/{alert.which}'
        alert.save()
        return JsonResponse({'message': 'Customer Debited Successfully'})

@staff_member_required(login_url='staff_login')
def CustomerTransferView(request, pk):
    unread_conversation = Conversation.objects.annotate(
        unread_messages_count = Count('chat', filter=~Q(chat__sender=request.user) & Q(chat__read=False))
    ).filter(
        participants=request.user,
        unread_messages_count__gt=0
    ).count()
    account = CustomerAccount.objects.get(id=pk)
    if request.method == 'POST':
        receiver = request.POST['receiver']
        amount = request.POST['amount']
        purpose = request.POST['purpose']
        if len(receiver) > 10 or len(receiver) < 10:
            messages.error(request, "Length Of Account Number Should Be 10")
            return redirect(reverse('customertransfer', args=[account.pk]))
        if CustomerAccount.objects.filter(account_number=int(receiver)).exists() == False:
            messages.error(request, "Receiver's Account Not Found")
            return redirect(reverse('customertransfer', args=[account.pk]))
        if account.user.balance < float(amount):
            messages.error(request, "Insufficient Funds")
            return redirect(reverse('customertransfer', args=[account.pk]))
        receiver_account = CustomerAccount.objects.get(account_number=receiver)
        if receiver_account == account:
            messages.error(request, 'You Cannot Transfer From Customer To Thesame Customer')
            return redirect(reverse('customertransfer', args=[account.pk]))
        if 'add' in request.POST:
            if Beneficiary.objects.filter(confirm=True, account=account, beneficiary=receiver_account).exists():
                messages.error(request, 'Receiver Is Already A Beneficiary')
            else:
                new = Beneficiary(confirm=True, account=account, beneficiary=receiver_account)
                new.save()
                messages.success(request, 'Receiver Successfully Added To Beneficiaries')
        transfer = Transfer(sender=account, txn_id=generate_transfer_id(), receiver=receiver_account, amount=float(amount), purpose=purpose)
        transfer.save()
        transfer.user.add(account.user)
        transfer.user.add(receiver_account.user)
        messages.info(request, 'Confirm Transaction')
        return redirect(reverse('customerconfirmtransfer', args=[transfer.pk]))
    context = {
        'account':account,
        'unread_conversation':unread_conversation,
        }
    return render(request, 'staff/customertransfer.html', context)

@staff_member_required(login_url='staff_login')
def CustomerConfirmTransferView(request, pk):
    unread_conversation = Conversation.objects.annotate(
        unread_messages_count = Count('chat', filter=~Q(chat__sender=request.user) & Q(chat__read=False))
    ).filter(
        participants=request.user,
        unread_messages_count__gt=0
    ).count()
    transfer = Transfer.objects.get(id=pk)
    if request.method == 'POST':
        transfer.sender.user.balance -= transfer.amount
        transfer.sender.user.save()
        data = Alert(amount=transfer.amount, balance=transfer.sender.user.balance, user=transfer.sender.user, transfer=transfer, txn='Debit', how='Mobile', which='UTU')
        data.detail = f'{data.transfer.txn_id}/{data.how}/{data.which}/Transfer'
        data.save()
        transfer.receiver.user.balance += transfer.amount
        transfer.receiver.user.save()
        data1 = Alert(amount=transfer.amount, balance=transfer.receiver.user.balance, user=transfer.receiver.user, transfer=transfer, txn='Credit', how='Mobile', which='UTU')
        data1.detail = f'{data.transfer.txn_id}/{data.how}/{data.which}/Transfer'
        data1.save()
        transfer.status = 'Completed'
        transfer.save()
        if transfer.sender.user.email_notification == True:
            subject = 'Patridge Bank: Transfer Successful'
            email_template_name = 'mail/transfer_success.txt'
            current_site = get_current_site(request)
            context = {
            'domain': current_site.domain,
            "user": transfer.sender.user,
            "transfer": transfer,
            }
            email = render_to_string(email_template_name, context)
            try:
                msg = EmailMultiAlternatives(subject, email, settings.EMAIL_HOST_USER , [transfer.sender.user.email])
                msg.send()
            except BadHeaderError:
                return redirect('Invalid header found.')
        if transfer.receiver.user.email_notification == True:
            subject = 'Patridge Bank: Transfer Credit Alert'
            email_template_name = 'mail/transfer_credit.txt'
            current_site = get_current_site(request)
            context = {
            'domain': current_site.domain,
            "user": transfer.receiver.user,
            "transfer": transfer,
            }
            email = render_to_string(email_template_name, context)
            try:
                msg = EmailMultiAlternatives(subject, email, settings.EMAIL_HOST_USER , [transfer.receiver.user.email])
                msg.send()
            except BadHeaderError:
                return redirect('Invalid header found.')
        messages.success(request, f'Transfer Of ₦{transfer.amount} To {transfer.receiver.account_name} Is Successful')
        return redirect(reverse('customerdetail', args=[transfer.sender.account_number]))
    context = {
        'unread_conversation':unread_conversation,
        'transfer':transfer,
        'confirmtransfer':'confirmtransfer'
        }
    return render(request, 'staff/customerconfirmtransfer.html', context)

@staff_member_required(login_url='staff_login')
def CustomerBillView(request, pk):
    unread_conversation = Conversation.objects.annotate(
        unread_messages_count = Count('chat', filter=~Q(chat__sender=request.user) & Q(chat__read=False))
    ).filter(
        participants=request.user,
        unread_messages_count__gt=0
    ).count()
    account = CustomerAccount.objects.get(id=pk)
    context = {
        'unread_conversation':unread_conversation,
        'account':account
        }
    return render(request, 'staff/customerbillpayment.html', context)

@staff_member_required(login_url='staff_login')
def CustomerCablePaymentView(request, pk):
    unread_conversation = Conversation.objects.annotate(
        unread_messages_count = Count('chat', filter=~Q(chat__sender=request.user) & Q(chat__read=False))
    ).filter(
        participants=request.user,
        unread_messages_count__gt=0
    ).count()
    account = CustomerAccount.objects.get(id=pk)
    form = CableForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            obj = form.save(commit=False)
            obj.account = account
            obj.save()
            bill = Bill(account=account, txn_id=generate_bill_id(), cable=obj)
            bill.save()
            if bill.cable.service.name == 'GOTV':
                result = MNCable.gotv_get_details(pk=bill.pk)
            if bill.cable.service.name == 'DSTV':
                result = MNCable.dstv_get_details(pk=bill.pk)
            if bill.cable.service.name == 'Startimes':
                result = MNCable.startimes_get_details(pk=bill.pk)
            if result == 'Error':
                messages.error(request, 'An Error Occurred. Check The Card Number And Try Again.')
                return redirect(reverse('customercable', args=[account.pk]))
            messages.info(request, 'Confirm Transaction')
            return redirect(reverse('customerconfirmbill', args=[bill.pk]))
    return render(request, 'staff/customercablepayment.html', {'unread_conversation':unread_conversation, 'form':form, 'account':account})

@staff_member_required(login_url='staff_login')
def CustomerElectricityPaymentView(request, pk):
    unread_conversation = Conversation.objects.annotate(
        unread_messages_count = Count('chat', filter=~Q(chat__sender=request.user) & Q(chat__read=False))
    ).filter(
        participants=request.user,
        unread_messages_count__gt=0
    ).count()
    account = CustomerAccount.objects.get(id=pk)
    form = ElectricityForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            obj = form.save(commit=False)
            obj.account = account
            obj.save()
            bill = Bill(account=account, txn_id=generate_bill_id(), electricity=obj)
            bill.save()
            messages.info(request, 'Confirm Transaction')
            return redirect(reverse('customerconfirmbill', args=[bill.pk]))
    return render(request, 'staff/customerelectricitypayment.html', {'unread_conversation':unread_conversation, 'form':form, 'account':account})

@staff_member_required(login_url='staff_login')
def CustomerConfirmBillView(request, pk):
    unread_conversation = Conversation.objects.annotate(
        unread_messages_count = Count('chat', filter=~Q(chat__sender=request.user) & Q(chat__read=False))
    ).filter(
        participants=request.user,
        unread_messages_count__gt=0
    ).count()
    bill = Bill.objects.get(id=pk)
    if bill.cable:
        if bill.cable.service.name == 'GOTV':
            result = MNCable.gotv_get_details(pk=bill.pk)
            if result == 'Error':
                messages.error(request, 'An Error Occurred. Check The Card Number And Try Again.')
                return redirect(reverse('customercable', args=[bill.account.pk]))
            detail = result
            name = detail['firstName'] + ' ' + detail['lastName']
            customerType = detail['customerType']
            dueDate = detail['dueDate']
            returnCode = None
            accountStatus = detail['accountStatus']
            invoicePeriod = detail['invoicePeriod']
            customerNumber = detail['customerNumber']
            if bill.cable.plan:
                amount = bill.amount
                if bill.cable.service.name == 'GOTV':
                    old_plan = get_closest_plan('GOTV', amount)
                if bill.cable.service.name == 'DSTV':
                    old_plan = get_closest_plan('DSTV', amount)
                if bill.cable.service.name == 'Startimes':
                    old_plan = get_closest_plan('Startimes', amount)
                new_plan = bill.cable.plan
                old_amount = old_plan.amount
                new_amount = bill.cable.plan.amount
            else:
                amount = bill.amount
                if bill.cable.service.name == 'GOTV':
                    old_plan = get_closest_plan('GOTV', amount)
                if bill.cable.service.name == 'DSTV':
                    old_plan = get_closest_plan('DSTV', amount)
                if bill.cable.service.name == 'Startimes':
                    old_plan = get_closest_plan('Startimes', amount)
                new_plan = old_plan
                old_amount = old_plan.amount
                new_amount = old_amount
                bill.cable.plan = old_plan
                bill.cable.save()
            bill.cable.customer_name = name
            bill.cable.customer_number = customerNumber
            bill.cable.save()
            bill.amount = new_amount
            bill.save()
        if bill.cable.service.name == 'DSTV':
            result = MNCable.dstv_get_details(pk=bill.pk)
            if result == 'Error':
                messages.error(request, 'An Error Occurred. Check The Card Number And Try Again.')
                return redirect(reverse('customercable', args=[bill.account.pk]))
            detail = result
            name = detail['firstName'] + ' ' + detail['lastName']
            customerType = detail['customerType']
            dueDate = detail['dueDate']
            returnCode = None
            accountStatus = detail['accountStatus']
            invoicePeriod = detail['invoicePeriod']
            customerNumber = detail['customerNumber']
            if bill.cable.plan:
                amount = bill.amount
                if bill.cable.service.name == 'GOTV':
                    old_plan = get_closest_plan('GOTV', amount)
                if bill.cable.service.name == 'DSTV':
                    old_plan = get_closest_plan('DSTV', amount)
                if bill.cable.service.name == 'Startimes':
                    old_plan = get_closest_plan('Startimes', amount)
                new_plan = bill.cable.plan
                old_amount = old_plan.amount
                new_amount = bill.cable.plan.amount
            else:
                amount = bill.amount
                if bill.cable.service.name == 'GOTV':
                    old_plan = get_closest_plan('GOTV', amount)
                if bill.cable.service.name == 'DSTV':
                    old_plan = get_closest_plan('DSTV', amount)
                if bill.cable.service.name == 'Startimes':
                    old_plan = get_closest_plan('Startimes', amount)
                new_plan = old_plan
                old_amount = old_plan.amount
                new_amount = old_amount
                bill.cable.plan = old_plan
                bill.cable.save()
            bill.cable.customer_name = name
            bill.cable.customer_number = customerNumber
            bill.cable.save()
            bill.amount = new_amount
            bill.save()
        if bill.cable.service.name == 'Startimes':
            result = MNCable.startimes_get_details(pk=bill.pk)
            if result == 'Error':
                messages.error(request, 'An Error Occurred. Check The Card Number And Try Again.')
                return redirect(reverse('customercable', args=[bill.account.pk]))
            detail = result
            name = detail['customerName']
            customerType = detail['customerType']
            dueDate = None
            returnCode = detail['returnCode']
            accountStatus = None
            invoicePeriod = None
            customerNumber = detail['customerNumber']
            if bill.cable.plan:
                amount = bill.amount
                if bill.cable.service.name == 'GOTV':
                    old_plan = get_closest_plan('GOTV', amount)
                if bill.cable.service.name == 'DSTV':
                    old_plan = get_closest_plan('DSTV', amount)
                if bill.cable.service.name == 'Startimes':
                    old_plan = get_closest_plan('Startimes', amount)
                new_plan = bill.cable.plan
                old_amount = old_plan.amount
                new_amount = bill.cable.plan.amount
            else:
                amount = bill.amount
                if bill.cable.service.name == 'GOTV':
                    old_plan = get_closest_plan('GOTV', amount)
                if bill.cable.service.name == 'DSTV':
                    old_plan = get_closest_plan('DSTV', amount)
                if bill.cable.service.name == 'Startimes':
                    old_plan = get_closest_plan('Startimes', amount)
                new_plan = old_plan
                old_amount = old_plan.amount
                new_amount = old_amount
                bill.cable.plan = old_plan
                bill.cable.save()
            bill.cable.customer_name = name
            bill.cable.customer_number = customerNumber
            bill.cable.save()
            bill.amount = new_amount
            bill.save()
        if request.method == 'POST':
            if bill.account.user.balance < bill.amount:
                messages.error(request, 'Insufficient Funds')
                return redirect(reverse('customercable', args=[bill.account.pk]))
            else:
                if bill.cable.service.name == 'GOTV':
                    MNCable.gotv_recharge(request, pk=bill.pk)
                if bill.cable.service.name == 'DSTV':
                    MNCable.dstv_recharge(request, pk=bill.pk)
                if bill.cable.service.name == 'Startimes':
                    MNCable.startimes_recharge(request, pk=bill.pk)
            return redirect(reverse('customerdetail', args=[bill.account.account_number]))
        context = {
            'unread_conversation':unread_conversation,
            'bill':bill,
            'name':name,
            'customerType':customerType,
            'dueDate':dueDate,
            'returnCode':returnCode,
            'accountStatus':accountStatus,
            'invoicePeriod':invoicePeriod,
            'customerNumber':customerNumber,
            'old_amount':old_amount,
            'new_amount':new_amount,
            'old_plan':old_plan,
            'new_plan':new_plan
            }
        return render(request, 'staff/customerconfirmbill.html', context)
    if bill.electricity:
        if bill.electricity.service.name == 'Eko Electricity Prepaid':
            result = MNElectricity.eko_get_details(pk=bill.pk)
            if result == 'Error':
                messages.error(request, 'An Error Occurred. Check The Meter Number And Try Again.')
                return redirect(reverse('customerelectricity', args=[bill.account.pk]))
            detail = result
            name = detail['customerName']
            customerAddress = detail['customerAddress']
            customerDistrict = detail['customerDistrict']
            status = detail['status']
            responseMessage = detail['responseMessage']
            customerReference = None
            minimumVend = None
            tariff = None
            freeUnits = None
            outstandingAmount = None
            amount = bill.electricity.amount
            bill.electricity.customer_name = name
            bill.electricity.customer_address = customerAddress
            bill.electricity.customer_district = customerDistrict
            bill.electricity.save()
            bill.amount = amount
            bill.save()
        if bill.electricity.service.name == 'Abuja Electricity Prepaid':
            result = MNElectricity.abuja_get_details(pk=bill.pk)
            if result == 'Error':
                messages.error(request, 'An Error Occurred. Check The Meter Number And Try Again.')
                return redirect(reverse('customerelectricity', args=[bill.account.pk]))
            detail = result
            name = detail['customerName']
            customerAddress = detail['customerAddress']
            customerDistrict = None
            status = None
            customerReference = detail['customerReference']
            minimumVend = detail['minimumVend']
            tariff = detail['tariff']
            responseMessage = detail['responseMessage']
            freeUnits = None
            outstandingAmount = None
            amount = bill.electricity.amount
            bill.electricity.customer_name = name
            bill.electricity.customer_address = customerAddress
            bill.electricity.customer_reference = customerReference
            bill.electricity.save()
            bill.amount = amount
            bill.save()
        if bill.electricity.service.name == 'Kaduna Electricity Prepaid':
            result = MNElectricity.kaduna_get_details(pk=bill.pk)
            if result == 'Error':
                messages.error(request, 'An Error Occurred. Check The Meter Number And Try Again.')
                return redirect(reverse('customerelectricity', args=[bill.account.pk]))
            detail = result
            name = detail['customerName']
            customerAddress = detail['customerAddress']
            customerDistrict = None
            status = None
            customerReference = None
            minimumVend = detail['minimumAmount']
            tariff = detail['tariff']
            responseMessage = detail['responseMessage']
            freeUnits = detail['freeUnits']
            outstandingAmount = detail['outstandingAmount']
            amount = bill.electricity.amount
            bill.electricity.customer_name = name
            bill.electricity.customer_address = customerAddress
            bill.electricity.tariff_code = tariff
            bill.electricity.save()
            bill.amount = amount
            bill.save()
        if bill.electricity.service.name == 'Ibadan Electricity Prepaid':
            result = MNElectricity.ibadan_get_details(pk=bill.pk)
            if result == 'Error':
                messages.error(request, 'An Error Occurred. Check The Meter Number And Try Again.')
                return redirect(reverse('customerelectricity', args=[bill.account.pk]))
            detail = result
            name = detail['customerName']
            customerAddress = detail['customerAddress']
            customerDistrict = None
            status = None
            customerReference = None
            minimumVend = detail['minimumAmount']
            tariff = detail['tariff']
            responseMessage = detail['responseMessage']
            freeUnits = detail['freeUnits']
            outstandingAmount = detail['outstandingAmount']
            amount = bill.electricity.amount
            bill.electricity.customer_name = name
            if customerAddress:
                bill.electricity.customer_address = customerAddress
            bill.electricity.save()
            bill.amount = amount
            bill.save()
        if request.method == 'POST':
            if bill.account.user.balance < bill.amount:
                messages.error(request, 'Insufficient Funds')
                return redirect(reverse('customerelectricity', args=[bill.account.pk]))
            else:
                if bill.electricity.service.name == 'Eko Electricity Prepaid':
                    MNElectricity.eko_recharge(request, pk=bill.pk)
                if bill.electricity.service.name == 'Abuja Electricity Prepaid':
                    MNElectricity.abuja_recharge(request, pk=bill.pk)
                if bill.electricity.service.name == 'Kaduna Electricity Prepaid':
                    MNElectricity.kaduna_recharge(request, pk=bill.pk)
                if bill.electricity.service.name == 'Ibadan Electricity Prepaid':
                    MNElectricity.ibadan_recharge(request, pk=bill.pk)
            return redirect(reverse('customerdetail', args=[bill.account.account_number]))
        context = {
            'unread_conversation':unread_conversation,
            'bill':bill,
            'name':name,
            'customerAddress':customerAddress,
            'customerDistrict':customerDistrict,
            'status':status,
            'responseMessage':responseMessage,
            'customerReference':customerReference,
            'minimumVend':minimumVend,
            'tariff':tariff,
            'freeUnits':freeUnits,
            'outstandingAmount':outstandingAmount,
            'amount':amount,
            }
        return render(request, 'staff/customerconfirmbill.html', context)

@staff_member_required(login_url='staff_login')
def CustomerTopUpView(request, pk):
    unread_conversation = Conversation.objects.annotate(
        unread_messages_count = Count('chat', filter=~Q(chat__sender=request.user) & Q(chat__read=False))
    ).filter(
        participants=request.user,
        unread_messages_count__gt=0
    ).count()
    account = CustomerAccount.objects.get(id=pk)
    context = {
        'unread_conversation':unread_conversation,
        'account':account
        }
    return render(request, 'staff/customertopuppayment.html', context)

@staff_member_required(login_url='staff_login')
def CustomerAirtimeView(request, pk):
    unread_conversation = Conversation.objects.annotate(
        unread_messages_count = Count('chat', filter=~Q(chat__sender=request.user) & Q(chat__read=False))
    ).filter(
        participants=request.user,
        unread_messages_count__gt=0
    ).count()
    account = CustomerAccount.objects.get(id=pk)
    providers = Provider.objects.all()

    # Create a dictionary to store service statuses
    provider_statuses = {}

    # Loop through the services and fetch their statuses using the custom method
    for provider in providers:
        status = get_airtime_status(provider.name)
        provider_statuses[provider.name] = status

    form = AirtimeForm(request.POST or None, provider_statuses=provider_statuses)
    
    if request.method == 'POST':
        if form.is_valid():
            obj = form.save(commit=False)
            obj.account = account
            if account.user.balance < obj.amount:
                messages.error(request, "Insufficient Funds")
                return redirect(reverse('customerairtime', args=[account.pk]))
            if len(obj.phone_number) > 11 or len(obj.phone_number) < 11:
                messages.error(request, 'Phone Number Should Be 11 Digits')
                return redirect(reverse('customerairtime', args=[account.pk]))
            obj.save()
            topup = TopUp(account=account, txn_id=generate_topup_id(), airtime=obj, amount=obj.amount, phone_number=obj.phone_number)
            topup.save()
            messages.info(request, 'Confirm Transaction')
            return redirect(reverse('customerconfirmtop', args=[topup.pk]))
    return render(request, 'staff/customerairtimepayment.html', {'unread_conversation':unread_conversation, 'form':form, 'account':account})

@staff_member_required(login_url='staff_login')
def CustomerDataView(request, pk):
    unread_conversation = Conversation.objects.annotate(
        unread_messages_count = Count('chat', filter=~Q(chat__sender=request.user) & Q(chat__read=False))
    ).filter(
        participants=request.user,
        unread_messages_count__gt=0
    ).count()
    account = CustomerAccount.objects.get(id=pk)
    providers = Provider.objects.all()
    
    # Create a dictionary to store service statuses
    provider_statuses = {}

    # Loop through the services and fetch their statuses using the custom method
    for provider in providers:
        status = get_data_status(provider.name)
        provider_statuses[provider.id] = (provider.name, status)
    
    form = DataForm(request.POST or None, provider_statuses=provider_statuses)
    if request.method == 'POST':
        if form.is_valid():
            obj = form.save(commit=False)
            obj.account = account
            if account.user.balance < obj.plan.amount:
                messages.error(request, "Insufficient Funds")
                return redirect(reverse('customerdata', args=[account.pk]))
            if len(obj.phone_number) > 11 or len(obj.phone_number) < 11:
                messages.error(request, 'Phone Number Should Be 11 Digits')
                return redirect(reverse('customerdata', args=[account.pk]))
            obj.save()
            topup = TopUp(account=account, txn_id=generate_topup_id(), data=obj, amount=obj.plan.amount, phone_number=obj.phone_number)
            topup.save()
            messages.info(request, 'Confirm Transaction')
            return redirect(reverse('customerconfirmtop', args=[topup.pk]))
    return render(request, 'staff/customerdatapayment.html', {'unread_conversation':unread_conversation, 'form':form, 'account':account})

@staff_member_required(login_url='staff_login')
def CustomerConfirmTopView(request, pk):
    unread_conversation = Conversation.objects.annotate(
        unread_messages_count = Count('chat', filter=~Q(chat__sender=request.user) & Q(chat__read=False))
    ).filter(
        participants=request.user,
        unread_messages_count__gt=0
    ).count()
    topup = TopUp.objects.get(id=pk)
    if request.method == 'POST':
        if topup.airtime:
            if topup.airtime.service.name == 'MTN':
                MNAirtimeRecharge.mtn_recharge(request, topup_id=pk)
            elif topup.airtime.service.name == '9MOBILE':
                MNAirtimeRecharge.etisalat_recharge(request, topup_id=pk)
            elif topup.airtime.service.name == 'GLO':
                MNAirtimeRecharge.glo_recharge(request, topup_id=pk)
            elif topup.airtime.service.name == 'AIRTEL':
                MNAirtimeRecharge.airtel_recharge(request, topup_id=pk)
        elif topup.data:
            if topup.data.service.name == 'MTN':
                MNDataRecharge.mtn_recharge(request, topup_id=pk)
            elif topup.data.service.name == '9MOBILE':
                MNDataRecharge.etisalat_recharge(request, topup_id=pk)
            elif topup.data.service.name == 'GLO':
                MNDataRecharge.glo_recharge(request, topup_id=pk)
            elif topup.data.service.name == 'AIRTEL':
                MNDataRecharge.airtel_recharge(request, topup_id=pk)
        return redirect(reverse('customerdetail', args=[topup.account.account_number]))
    context = {
        'unread_conversation':unread_conversation,
        'topup':topup,
        }
    return render(request, 'staff/customerconfirmtopup.html', context)

@staff_member_required(login_url='staff_login')
def TransactionChartView(request, pk):
    unread_conversation = Conversation.objects.annotate(
        unread_messages_count = Count('chat', filter=~Q(chat__sender=request.user) & Q(chat__read=False))
    ).filter(
        participants=request.user,
        unread_messages_count__gt=0
    ).count()
    account = CustomerAccount.objects.get(id=pk)
    debit_transactions = Alert.objects.filter(user=account.user, txn='Debit')
    credit_transactions = Alert.objects.filter(user=account.user, txn='Credit')
    debit_amount = sum(debit_transaction.amount for debit_transaction in debit_transactions)
    credit_amount = sum(credit_transaction.amount for credit_transaction in credit_transactions)
    transfer_transactions = Alert.objects.filter(user=account.user, transfer__sender=account)
    bill_transactions = Alert.objects.filter(user=account.user, bill__account=account)
    topup_transactions = Alert.objects.filter(user=account.user, topup__account=account)
    transfer_amount = sum(transfer_transaction.amount for transfer_transaction in transfer_transactions)
    bill_amount = sum(bill_transaction.amount for bill_transaction in bill_transactions)
    topup_amount = sum(topup_transaction.amount for topup_transaction in topup_transactions)
    context = {
        'unread_conversation':unread_conversation,
        'account':account,
        'nofilter':'nofilter',
        'credit_amount':credit_amount,
        'debit_amount':debit_amount,
        'transfer_amount':transfer_amount,
        'bill_amount':bill_amount,
        'topup_amount':topup_amount
    }
    return render(request, 'staff/demographics.html', context)

@staff_member_required(login_url='staff_login')
def DateTxnFilterView(request, start, stop, pk):
    unread_conversation = Conversation.objects.annotate(
        unread_messages_count = Count('chat', filter=~Q(chat__sender=request.user) & Q(chat__read=False))
    ).filter(
        participants=request.user,
        unread_messages_count__gt=0
    ).count()
    account = CustomerAccount.objects.get(id=pk)
    debit_transactions = Alert.objects.filter(user=account.user, txn='Debit', date__date__range=(start, stop))
    credit_transactions = Alert.objects.filter(user=account.user, txn='Credit', date__date__range=(start, stop))
    debit_amount = sum(debit_transaction.amount for debit_transaction in debit_transactions)
    credit_amount = sum(credit_transaction.amount for credit_transaction in credit_transactions)
    transfer_transactions = Alert.objects.filter(user=account.user, transfer__sender=account)
    bill_transactions = Alert.objects.filter(user=account.user, bill__account=account)
    topup_transactions = Alert.objects.filter(user=account.user, topup__account=account)
    transfer_amount = sum(transfer_transaction.amount for transfer_transaction in transfer_transactions)
    bill_amount = sum(bill_transaction.amount for bill_transaction in bill_transactions)
    topup_amount = sum(topup_transaction.amount for topup_transaction in topup_transactions)
    context = {
        'unread_conversation':unread_conversation,
        'credit_amount':credit_amount,
        'debit_amount':debit_amount,
        'account':account,
        'start':start,
        'stop':stop,
        'datefilter':'datefilter',
        'transfer_amount':transfer_amount,
        'bill_amount':bill_amount,
        'topup_amount':topup_amount
    }
    return render(request, 'staff/demographics.html', context)

@staff_member_required(login_url='staff_login')
def DateUtilityFilterView(request, start, stop, pk):
    unread_conversation = Conversation.objects.annotate(
        unread_messages_count = Count('chat', filter=~Q(chat__sender=request.user) & Q(chat__read=False))
    ).filter(
        participants=request.user,
        unread_messages_count__gt=0
    ).count()
    account = CustomerAccount.objects.get(id=pk)
    debit_transactions = Alert.objects.filter(user=account.user, txn='Debit')
    credit_transactions = Alert.objects.filter(user=account.user, txn='Credit')
    debit_amount = sum(debit_transaction.amount for debit_transaction in debit_transactions)
    credit_amount = sum(credit_transaction.amount for credit_transaction in credit_transactions)
    transfer_transactions = Alert.objects.filter(user=account.user, transfer__sender=account, date__date__range=(start, stop))
    bill_transactions = Alert.objects.filter(user=account.user, bill__account=account, date__date__range=(start, stop))
    topup_transactions = Alert.objects.filter(user=account.user, topup__account=account, date__date__range=(start, stop))
    transfer_amount = sum(transfer_transaction.amount for transfer_transaction in transfer_transactions)
    bill_amount = sum(bill_transaction.amount for bill_transaction in bill_transactions)
    topup_amount = sum(topup_transaction.amount for topup_transaction in topup_transactions)
    context = {
        'unread_conversation':unread_conversation,
        'credit_amount':credit_amount,
        'debit_amount':debit_amount,
        'account':account,
        'start':start,
        'stop':stop,
        'dateutilfilter':'dateutilfilter',
        'transfer_amount':transfer_amount,
        'bill_amount':bill_amount,
        'topup_amount':topup_amount
    }
    return render(request, 'staff/demographics.html', context)

@staff_member_required(login_url='staff_login')
def ManageCustomerBeneficiaryView(request, pk):
    unread_conversation = Conversation.objects.annotate(
        unread_messages_count = Count('chat', filter=~Q(chat__sender=request.user) & Q(chat__read=False))
    ).filter(
        participants=request.user,
        unread_messages_count__gt=0
    ).count()
    account = CustomerAccount.objects.get(id=pk)
    beneficiary = Beneficiary.objects.filter(account=account, confirm=True)
    return render(request, 'staff/customerbeneficiary.html', {'unread_conversation':unread_conversation, 'account':account, 'beneficiary':beneficiary})

@staff_member_required(login_url='staff_login')
def RemoveCustomerBeneficiaryView(request, pk):
    account = CustomerAccount.objects.get(id=pk)
    if request.method == 'POST':
        beneficiary_id = request.POST.get('beneficiary_id')
        try:
            obj = Beneficiary.objects.get(id=beneficiary_id)
            obj.delete()
            return redirect(reverse('managebene', args=[account.pk]))
        except Beneficiary.DoesNotExist:
            pass
        except Exception as e:
            pass
    return redirect(reverse('managebene', args=[account.pk]))

@staff_member_required(login_url='staff_login')
def AddCustomerBeneficiaryView(request, pk):
    unread_conversation = Conversation.objects.annotate(
        unread_messages_count = Count('chat', filter=~Q(chat__sender=request.user) & Q(chat__read=False))
    ).filter(
        participants=request.user,
        unread_messages_count__gt=0
    ).count()
    account = CustomerAccount.objects.get(id=pk)
    if request.method == 'POST':
        beneficiary_account_number = request.POST['account_number']
        if CustomerAccount.objects.filter(account_number=beneficiary_account_number).exists():
            beneficiary = CustomerAccount.objects.get(account_number=beneficiary_account_number)
        else:
            messages.error(request, 'No Customer Account Found. Check The Account Number Inputted')
            return redirect(reverse('addbene', args=[account.pk]))
        if Beneficiary.objects.filter(account=account, beneficiary=beneficiary).exists():
            messages.error(request, f'Beneficiary Already Added - {beneficiary.account_name}/{beneficiary.account_number}')
            return redirect(reverse('managebene', args=[account.pk]))
        if beneficiary == account:
            messages.error(request, "You Cannot Add Customer To Thesame Customer's Beneficiaries")
            return redirect(reverse('addbene', args=[account.pk]))
        else:
            new = Beneficiary(account=account, beneficiary=beneficiary)
            new.save()
            messages.success(request, 'Confirm Beneficiary')
            return redirect(reverse('confirmbene', args=[new.pk]))
    return render(request, 'staff/addcustomerbeneficiary.html', {'unread_conversation':unread_conversation, 'account':account})

@staff_member_required(login_url='staff_login')
def ConfirmCustomerBeneficiaryView(request, pk):
    unread_conversation = Conversation.objects.annotate(
        unread_messages_count = Count('chat', filter=~Q(chat__sender=request.user) & Q(chat__read=False))
    ).filter(
        participants=request.user,
        unread_messages_count__gt=0
    ).count()
    beneficiary = Beneficiary.objects.get(id=pk)
    if request.method == 'POST':
        beneficiary.confirm = True
        beneficiary.save()
        if beneficiary.account.user.email_notification == True:
            subject = 'Patridge Bank: Beneficiary Added Successfully'
            email_template_name = 'mail/beneficiary_success.txt'
            current_site = get_current_site(request)
            context = {
            'domain': current_site.domain,
            "user": beneficiary.account.user,
            "beneficiary": beneficiary,
            'date': timezone.now().date()
            }
            email = render_to_string(email_template_name, context)
            try:
                msg = EmailMultiAlternatives(subject, email, settings.EMAIL_HOST_USER , [beneficiary.account.user.email])
                msg.send()
            except BadHeaderError:
                return redirect('Invalid header found.')
        messages.success(request, 'Beneficiary Added Successfully')
        return redirect(reverse('managebene', args=[beneficiary.account.pk]))
    return render(request, 'staff/confirmcustomerbeneficiary.html', {'unread_conversation':unread_conversation, 'beneficiary':beneficiary, 'account':beneficiary.account, 'date':timezone.now().date()})

@staff_member_required(login_url='staff_login')
def CustomerBeneficiaryTransferView(request, pk, id):
    unread_conversation = Conversation.objects.annotate(
        unread_messages_count = Count('chat', filter=~Q(chat__sender=request.user) & Q(chat__read=False))
    ).filter(
        participants=request.user,
        unread_messages_count__gt=0
    ).count()
    account = CustomerAccount.objects.get(id=pk)
    beneficiary = Beneficiary.objects.get(id=id)
    if request.method == 'POST':
        receiver = request.POST['receiver']
        amount = request.POST['amount']
        purpose = request.POST['purpose']
        if len(receiver) > 10 or len(receiver) < 10:
            messages.error(request, "Length Of Account Number Should Be 10")
            return redirect(reverse('transfertocustomerbeneficiary', args=[account.pk, beneficiary.pk]))
        if CustomerAccount.objects.filter(account_number=int(receiver)).exists() == False:
            messages.error(request, "Receiver's Account Not Found")
            return redirect(reverse('transfertocustomerbeneficiary', args=[account.pk, beneficiary.pk]))
        if account.user.balance < float(amount):
            messages.error(request, "Insufficient Funds")
            return redirect(reverse('transfertocustomerbeneficiary', args=[account.pk, beneficiary.pk]))
        receiver_account = CustomerAccount.objects.get(account_number=receiver)
        transfer = Transfer(sender=account, txn_id=generate_transfer_id(), receiver=receiver_account, amount=float(amount), purpose=purpose)
        transfer.save()
        transfer.user.add(account.user)
        transfer.user.add(receiver_account.user)
        messages.info(request, 'Confirm Transaction')
        return redirect(reverse('customerconfirmtransfer', args=[transfer.pk]))
    context = {
        'account':account,
        'beneficiary':beneficiary,
        'benetransfer':'benetransfer',
        'unread_conversation':unread_conversation,
        }
    return render(request, 'staff/customerbeneficiarytransfer.html', context)

@staff_member_required(login_url='staff_login')
def CustomerStatementView(request, pk):
    unread_conversation = Conversation.objects.annotate(
        unread_messages_count = Count('chat', filter=~Q(chat__sender=request.user) & Q(chat__read=False))
    ).filter(
        participants=request.user,
        unread_messages_count__gt=0
    ).count()
    account = CustomerAccount.objects.get(id=pk)
    alert = Alert.objects.filter(user=account.user)
    if request.method == 'POST':
        start = request.POST['start']
        stop = request.POST['stop']
        if not 'doc' in request.POST and not 'email' in request.POST:
            messages.error(request, 'Choose A Method')
            return redirect(reverse('customer_statement', args=[account.pk]))
        if 'doc' in request.POST and 'email' in request.POST:
            messages.error(request, 'Choose Only One Method')
            return redirect(reverse('customer_statement', args=[account.pk]))
        if start > stop:
            messages.error(request, 'Stop Date Should Be Beyond Start Date')
            return redirect(reverse('customer_statement', args=[account.pk]))
        if stop > str(timezone.now().date()):
            messages.error(request, 'Date Should Not Be Beyond Today')
            return redirect(reverse('customer_statement', args=[account.pk]))
        if account.user.balance < float(100):
            messages.error(request, 'Insufficient Funds')
            return redirect(reverse('customerdetail', args=[account.account_number]))
        if 'doc' in request.POST and not 'email' in request.POST:
            if alert.filter(user=account.user, date__date__range=(start, stop)).exists():
                account.user.balance -= float(100)
                account.user.save()
                statement = Alert.objects.filter(user=account.user, date__date__range=(start, stop))
                debits = [float(debit.amount) for debit in statement if debit.txn == 'Debit']
                credits = [float(credit.amount) for credit in statement if credit.txn == 'Credit']
                total_debit = sum(debits) if debits else 0
                total_credit = sum(credits) if credits else 0

                buffer = BytesIO()
                doc = SimpleDocTemplate(buffer, pagesize=letter)
                elements = []
                styles = getSampleStyleSheet()

                # Add headings
                elements.append(Paragraph("Partridge Bank", styles['Title']))
                elements.append(Paragraph("Bank Statement", styles['Heading2']))

                # Add account details
                details = [
                    f"Account Name: {account.account_name}",
                    f"Account Number: {account.account_number}",
                    f"Date: {timezone.now().date()}",
                    f"Statement From: {start}",
                    f"Statement To: {stop}",
                    f"Total Credits: ₦{total_credit}",
                    f"Total Debits: ₦{total_debit}",
                    f"Latest Balance: ₦{account.user.balance}",
                ]
                for detail in details:
                    elements.append(Paragraph(detail, styles['Normal']))

                # Add transaction table
                data = [['Date', 'Transaction', 'Details', 'Amount(₦)', 'Balance(₦)']]
                for obj in statement:
                    data.append([
                        str(obj.date),
                        str(obj.txn),
                        str(obj.detail),
                        f"₦{obj.amount}",
                        f"₦{obj.balance}"
                    ])

                table = Table(data)
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ]))
                elements.append(table)

                # Build the PDF
                doc.build(elements)
                buffer.seek(0)
                response = FileResponse(buffer, content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename={account.account_name}_statement_{timezone.now().strftime("%Y%m%d")}.pdf'
                new = Alert(amount=float(100), balance=account.user.balance, user=account.user, statement=True, txn='Debit', how='Mobile', which='Patridge Bank')
                new.detail = f'Bank Statement/{new.how}/{new.which}'
                new.save()
                return response
            else:
                messages.error(request, 'No Transaction Occurred Within The Date Range Specified')
                return redirect(reverse('customer_statement', args=[account.pk]))
        if not 'doc' in request.POST and 'email' in request.POST:
            if alert.filter(user=account.user, date__date__range=(start, stop)).exists():
                account.user.balance -= float(100)
                account.user.save()
                subject = 'Patridge Bank: Bank Statement Request'
                email_template_name = 'mail/statement_success.txt'
                current_site = get_current_site(request)
                context = {
                'domain': current_site.domain,
                "user": account.user,
                "account": account,
                "start": start,
                "stop": stop,
                'date': timezone.now().date()
                }
                email = render_to_string(email_template_name, context)
                try:
                    msg = EmailMultiAlternatives(subject, email, settings.EMAIL_HOST_USER , [account.user.email])
                    msg.send()
                except BadHeaderError:
                    return redirect('Invalid header found.')
                new = Alert(amount=float(100), balance=account.user.balance, user=account.user, statement=True, txn='Debit', how='Mobile', which='Patridge Bank')
                new.detail = f'Bank Statement/{new.how}/{new.which}'
                new.save()
                messages.success(request, "Statement Request Successful. It Has Been Sent To Customer's Mail")
                return redirect(reverse('customerdetail', args=[account.account_number]))
            else:
                messages.error(request, 'No Transaction Occurred Within The Date Range Specified')
                return redirect(reverse('customer_statement', args=[account.pk]))
    return render(request, 'staff/requestcustomerstatement.html', {'unread_conversation':unread_conversation, 'account':account})

@staff_member_required(login_url='staff_login')
def CustomerMessageView(request, pk):
    unread_conversation = Conversation.objects.annotate(
        unread_messages_count = Count('chat', filter=~Q(chat__sender=request.user) & Q(chat__read=False))
    ).filter(
        participants=request.user,
        unread_messages_count__gt=0
    ).count()
    account = CustomerAccount.objects.get(id=pk)
    if request.method == 'POST':
        subject = request.POST['subject']
        body = request.POST['body']
        message = Message(user=account.user, message=f"{subject.upper()}: {body}")
        message.save()
        messages.success(request, 'Message Sent To Customer Successfully')
        return redirect(reverse('customerdetail', args=[account.account_number]))
    return render(request, 'staff/message.html', {'unread_conversation':unread_conversation, 'account':account})

@staff_member_required(login_url='staff_login')
def AllSupportView(request):
    unread_conversation = Conversation.objects.annotate(
        unread_messages_count = Count('chat', filter=~Q(chat__sender=request.user) & Q(chat__read=False))
    ).filter(
        participants=request.user,
        unread_messages_count__gt=0
    ).count()
    staffs = User.objects.filter(is_staff=True)
    customers = User.objects.filter(is_customer=True)
    support = Support.objects.exclude(staff__in=staffs).exclude(staff__in=customers).order_by('-date')
    paginator = Paginator(support, 20)
    page = request.GET.get('page')
    try:
        support = paginator.page(page)
    except PageNotAnInteger:
        support = paginator.page(1)
    except EmptyPage:
        support = paginator.page(paginator.num_pages)
    return render(request, 'staff/support.html', {'unread_conversation':unread_conversation, 'support':support})

@staff_member_required(login_url='staff_login')
def AnsweredSupportView(request):
    unread_conversation = Conversation.objects.annotate(
        unread_messages_count = Count('chat', filter=~Q(chat__sender=request.user) & Q(chat__read=False))
    ).filter(
        participants=request.user,
        unread_messages_count__gt=0
    ).count()
    staffs = User.objects.filter(is_staff=True)
    customers = User.objects.filter(is_customer=True)
    support = Support.objects.filter(answer=True).exclude(staff__in=staffs).exclude(staff__in=customers).order_by('-date')
    paginator = Paginator(support, 20)
    page = request.GET.get('page')
    try:
        support = paginator.page(page)
    except PageNotAnInteger:
        support = paginator.page(1)
    except EmptyPage:
        support = paginator.page(paginator.num_pages)
    return render(request, 'staff/support.html', {'unread_conversation':unread_conversation, 'support':support, 'answer':'answer'})

@staff_member_required(login_url='staff_login')
def NotAnsweredSupportView(request):
    unread_conversation = Conversation.objects.annotate(
        unread_messages_count = Count('chat', filter=~Q(chat__sender=request.user) & Q(chat__read=False))
    ).filter(
        participants=request.user,
        unread_messages_count__gt=0
    ).count()
    staffs = User.objects.filter(is_staff=True)
    customers = User.objects.filter(is_customer=True)
    support = Support.objects.filter(answer=False).exclude(staff__in=staffs).exclude(staff__in=customers).order_by('-date')
    paginator = Paginator(support, 20)
    page = request.GET.get('page')
    try:
        support = paginator.page(page)
    except PageNotAnInteger:
        support = paginator.page(1)
    except EmptyPage:
        support = paginator.page(paginator.num_pages)
    return render(request, 'staff/support.html', {'unread_conversation':unread_conversation, 'support':support, 'notanswer':'notanswer'})

@staff_member_required(login_url='staff_login')
def CustomerSupportView(request, pk):
    unread_conversation = Conversation.objects.annotate(
        unread_messages_count = Count('chat', filter=~Q(chat__sender=request.user) & Q(chat__read=False))
    ).filter(
        participants=request.user,
        unread_messages_count__gt=0
    ).count()
    customer = User.objects.get(id=pk)
    support = Support.objects.filter(customer=customer).order_by('date')
    paginator = Paginator(support, 10)
    last_page = paginator.num_pages
    page = request.GET.get('page', last_page)
    try:
        support = paginator.page(page)
    except PageNotAnInteger:
        support = paginator.page(1)
    except EmptyPage:
        support = paginator.page(paginator.num_pages)
    if request.method == 'POST':
        message = request.POST['message']
        new = Support(customer=customer, staff=request.user, message=message)
        new.save()
        message = Message(user=customer, message='Patridge Bank SUPPORT: Your Message In Support Has Been Replied')
        message.save()
        messages.success(request, 'reply sent')
        return redirect(reverse('answer_support', args=[customer.pk]))
    return render(request, 'staff/supportconversation.html', {'unread_conversation':unread_conversation, 'support':support})

@staff_member_required(login_url='staff_login')
def AnswerSupportView(pk):
    Support.objects.answer_support(customer_id=pk)
    return redirect(reverse('customer_support', args=[pk]))

@staff_member_required(login_url='staff_login')
def StaffChatView(request):
    unread_conversation = Conversation.objects.annotate(
        unread_messages_count = Count('chat', filter=~Q(chat__sender=request.user) & Q(chat__read=False))
    ).filter(
        participants=request.user,
        unread_messages_count__gt=0
    ).count()
    conversation = Conversation.objects.annotate(chat_count=Count('chat')).filter(chat_count__gt=0).filter(participants=request.user)
    conversation_timestamps = {}
    for convo in conversation:
        latest_message = Chat.objects.filter(conversation=convo).order_by('-date').first()
        conversation_timestamps[convo] = latest_message.date if latest_message else None
        convo.unread = Chat.objects.filter(conversation=convo, read=False).exclude(sender=request.user).count()
        convo.last = latest_message
        convo.other_staff = convo.participants.exclude(id=request.user.id).first()
        staff = StaffAccount.objects.get(user=convo.other_staff)
        convo.picture = staff.picture
    sorted_conversations = sorted(conversation, key=lambda c: conversation_timestamps[c], reverse=True)
    paginator = Paginator(sorted_conversations, 10)
    page = request.GET.get('page')
    try:
        sorted_conversations = paginator.page(page)
    except PageNotAnInteger:
        sorted_conversations = paginator.page(1)
    except EmptyPage:
        sorted_conversations = paginator.page(paginator.num_pages)
    if request.method == 'POST':
        data = request.POST['data']
        return redirect(reverse('search_chat', args=[data]))
    return render(request, 'staff/generalchat.html', {'unread_conversation':unread_conversation, 'conversation':sorted_conversations})

@staff_member_required(login_url='staff_login')
def SearchChatView(request, q):
    unread_conversation = Conversation.objects.annotate(
        unread_messages_count = Count('chat', filter=~Q(chat__sender=request.user) & Q(chat__read=False))
    ).filter(
        participants=request.user,
        unread_messages_count__gt=0
    ).count()
    staffs = User.objects.filter(staffaccount__account_name__icontains=q).exclude(user_ID=request.user.user_ID)
    if staffs.exists():
        for staff in staffs:
            conversation = Conversation.objects.annotate(chat_count=Count('chat')).filter(chat_count__gt=0).filter(participants=request.user).filter(participants=staff)
            if conversation.exists():
                conversation_timestamps = {}
                for convo in conversation:
                    latest_message = Chat.objects.filter(conversation=convo).order_by('-date').first()
                    conversation_timestamps[convo] = latest_message.date if latest_message else None
                    convo.unread = Chat.objects.filter(conversation=convo, read=False).exclude(sender=request.user).count()
                    convo.last = latest_message
                    convo.other_staff = convo.participants.exclude(id=request.user.id).first()
                    staff = StaffAccount.objects.get(user=convo.other_staff)
                    convo.picture = staff.picture
                sorted_conversations = sorted(conversation, key=lambda c: conversation_timestamps[c], reverse=True)
                paginator = Paginator(sorted_conversations, 10)
                page = request.GET.get('page')
                try:
                    sorted_conversations = paginator.page(page)
                except PageNotAnInteger:
                    sorted_conversations = paginator.page(1)
                except EmptyPage:
                    sorted_conversations = paginator.page(paginator.num_pages)
            else:
                messages.error(request, 'No Conversation Found')
                return redirect('staff_chat')
    else:
        messages.error(request, 'No Conversation Found')
        return redirect('staff_chat')
    return render(request, 'staff/searchchat.html', {'unread_conversation':unread_conversation, 'conversation':sorted_conversations})

@staff_member_required(login_url='staff_login')
def NewConversationView(request):
    unread_conversation = Conversation.objects.annotate(
        unread_messages_count = Count('chat', filter=~Q(chat__sender=request.user) & Q(chat__read=False))
    ).filter(
        participants=request.user,
        unread_messages_count__gt=0
    ).count()
    q = request.POST.get('q') if request.POST.get('q') != None else ''
    staffs = User.objects.filter(is_staff=True).exclude(user_ID=request.user.user_ID).filter(Q(staffaccount__account_name__icontains=q) | Q(user_ID__icontains=q)).order_by('id')
    staff_c = User.objects.filter(is_staff=True).exclude(user_ID=request.user.user_ID).filter(Q(staffaccount__account_name__icontains=q) | Q(user_ID__icontains=q)).count()
    for staff in staffs:
        try:
            account = StaffAccount.objects.get(user=staff)
            staff.picture = account.picture
        except(StaffAccount.DoesNotExist):
            staff.picture = None
    paginator = Paginator(staffs, 10)
    page = request.GET.get('page')
    try:
        staffs = paginator.page(page)
    except PageNotAnInteger:
        staffs = paginator.page(1)
    except EmptyPage:
        staffs = paginator.page(paginator.num_pages)
    return render(request, 'staff/newchat.html', {'unread_conversation':unread_conversation, 'staffs':staffs, 'staff_c':staff_c})

@staff_member_required(login_url='staff_login')
def ChatRoomView(request, pk):
    unread_conversation = Conversation.objects.annotate(
        unread_messages_count = Count('chat', filter=~Q(chat__sender=request.user) & Q(chat__read=False))
    ).filter(
        participants=request.user,
        unread_messages_count__gt=0
    ).count()
    conversation = Conversation.objects.get(id=pk)
    other_staff = conversation.participants.exclude(id=request.user.id).first()
    chat = Chat.objects.filter(conversation=conversation).order_by('date')
    for chit in chat:
        if chit.sender != request.user:
            Chat.objects.read_chat(chat_id=chit.id)
    paginator = Paginator(chat, 10)
    last_page = paginator.num_pages
    page = request.GET.get('page', last_page)
    try:
        chat = paginator.page(page)
    except PageNotAnInteger:
        chat = paginator.page(1)
    except EmptyPage:
        chat = paginator.page(paginator.num_pages)
    if request.method == 'POST':
        new = Chat(conversation=conversation, sender=request.user, message=request.POST['message'])
        new.save()
        return redirect(reverse('chat_room', args=[conversation.pk]))
    return render(request, 'staff/chatroom.html', {'unread_conversation':unread_conversation, 'chat':chat, 'other_staff':other_staff})

@staff_member_required(login_url='staff_login')
def StartConversationView(request, pk):
    other_staff = User.objects.get(id=pk)
    if Conversation.objects.filter(participants=request.user).filter(participants=other_staff).exists():
        conversation = Conversation.objects.filter(participants=request.user).filter(participants=other_staff).first()
        return redirect(reverse('chat_room', args=[conversation.pk]))
    else:
        new = Conversation()
        new.save()
        new.participants.add(request.user)
        new.participants.add(other_staff)
        return redirect(reverse('chat_room', args=[new.pk]))
