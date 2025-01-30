from django.conf import settings
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site 
from django.template.loader import render_to_string
from django.core.mail import BadHeaderError, EmailMultiAlternatives

from .models import *

import requests
import json

class MNAirtimeStatus:
    def mtn_get_status():
        public_key = settings.MOBILENIG_PUBLIC_KEY
        url = "https://enterprise.mobilenig.com/api/services/proxy"
        payload = json.dumps({
            "service_id": "BAD",
            "requestType": "PREMIUM"
        })
        headers = {
            "Content-Type": 'application/json',
            "Authorization": f'Bearer {public_key}'
        }
        response = requests.request('POST', url, headers=headers, data=payload)
        if response.status_code == 200:
            try:
                response_data = response.json()
                if response_data['details'].get('strength') == None:
                    return 'Status Not Available'
                else:
                    return response_data['details'].get('strength')
            except json.JSONDecodeError:
                print("Invalid JSON data")
        else:
            return 'Status Not Available'

    def etisalat_get_status():
        public_key = settings.MOBILENIG_PUBLIC_KEY
        url = "https://enterprise.mobilenig.com/api/services/proxy"
        payload = json.dumps({
            "service_id": "BAC",
            "requestType": "PREMIUM"
        })
        headers = {
            "Content-Type": 'application/json',
            "Authorization": f'Bearer {public_key}'
        }
        response = requests.request('POST', url, headers=headers, data=payload)
        if response.status_code == 200:
            try:
                response_data = response.json()
                if response_data['details'].get('strength') == None:
                    return 'Status Not Available'
                else:
                    return response_data['details'].get('strength')
            except json.JSONDecodeError:
                print("Invalid JSON data")
        else:
            return 'Status Not Available'

    def glo_get_status():
        public_key = settings.MOBILENIG_PUBLIC_KEY
        url = "https://enterprise.mobilenig.com/api/services/proxy"
        payload = json.dumps({
            "service_id": "BAB",
            "requestType": "PREMIUM"
        })
        headers = {
            "Content-Type": 'application/json',
            "Authorization": f'Bearer {public_key}'
        }
        response = requests.request('POST', url, headers=headers, data=payload)
        if response.status_code == 200:
            try:
                response_data = response.json()
                if response_data['details'].get('strength') == None:
                    return 'Status Not Available'
                else:
                    return response_data['details'].get('strength')
            except json.JSONDecodeError:
                print("Invalid JSON data")
        else:
            return 'Status Not Available'

    def airtel_get_status():
        public_key = settings.MOBILENIG_PUBLIC_KEY
        url = "https://enterprise.mobilenig.com/api/services/proxy"
        payload = json.dumps({
            "service_id": "BAA",
            "requestType": "PREMIUM"
        })
        headers = {
            "Content-Type": 'application/json',
            "Authorization": f'Bearer {public_key}'
        }
        response = requests.request('POST', url, headers=headers, data=payload)
        if response.status_code == 200:
            try:
                response_data = response.json()
                if response_data['details'].get('strength') == None:
                    return 'Status Not Available'
                else:
                    return response_data['details'].get('strength')
            except json.JSONDecodeError:
                print("Invalid JSON data")
        else:
            return 'Status Not Available'

class MNDataStatus:
    def mtn_get_status():
        public_key = settings.MOBILENIG_PUBLIC_KEY
        url = "https://enterprise.mobilenig.com/api/services/proxy"
        payload = json.dumps({
            "service_id": "BCA",
            "requestType": "SME"
        })
        headers = {
            "Content-Type": 'application/json',
            "Authorization": f'Bearer {public_key}'
        }
        response = requests.request('POST', url, headers=headers, data=payload)
        if response.status_code == 200:
            try:
                response_data = response.json()
                if response_data['details'].get('strength') == None:
                    return 'Status Not Available'
                else:
                    return response_data['details'].get('strength')
            except json.JSONDecodeError:
                print("Invalid JSON data")
        else:
            return 'Status Not Available'

    def etisalat_get_status():
        public_key = settings.MOBILENIG_PUBLIC_KEY
        url = "https://enterprise.mobilenig.com/api/services/proxy"
        payload = json.dumps({
            "service_id": "BCB",
            "requestType": "GIFTING"
        })
        headers = {
            "Content-Type": 'application/json',
            "Authorization": f'Bearer {public_key}'
        }
        response = requests.request('POST', url, headers=headers, data=payload)
        if response.status_code == 200:
            try:
                response_data = response.json()
                if response_data['details'].get('strength') == None:
                    return 'Status Not Available'
                else:
                    return response_data['details'].get('strength')
            except json.JSONDecodeError:
                print("Invalid JSON data")
        else:
            return 'Status Not Available'

    def glo_get_status():
        public_key = settings.MOBILENIG_PUBLIC_KEY
        url = "https://enterprise.mobilenig.com/api/services/proxy"
        payload = json.dumps({
            "service_id": "BCC",
            "requestType": "SME"
        })
        headers = {
            "Content-Type": 'application/json',
            "Authorization": f'Bearer {public_key}'
        }
        response = requests.request('POST', url, headers=headers, data=payload)
        if response.status_code == 200:
            try:
                response_data = response.json()
                if response_data['details'].get('status') == None:
                    return 'Status Not Available'
                else:
                    return response_data['details'].get('status')
            except json.JSONDecodeError:
                print("Invalid JSON data")
        else:
            return 'Status Not Available'

    def airtel_get_status():
        public_key = settings.MOBILENIG_PUBLIC_KEY
        url = "https://enterprise.mobilenig.com/api/services/proxy"
        payload = json.dumps({
            "service_id": "BCD",
            "requestType": "GIFTING"
        })
        headers = {
            "Content-Type": 'application/json',
            "Authorization": f'Bearer {public_key}'
        }
        response = requests.request('POST', url, headers=headers, data=payload)
        if response.status_code == 200:
            try:
                response_data = response.json()
                if response_data['details'].get('strength') == None:
                    return 'Status Not Available'
                else:
                    return response_data['details'].get('strength')
            except json.JSONDecodeError:
                print("Invalid JSON data")
        else:
            return 'Status Not Available'

class MNDataPlan:
    def mtn_get_plan():
        public_key = settings.MOBILENIG_PUBLIC_KEY
        url = "https://enterprise.mobilenig.com/api/services/packages"
        payload = json.dumps({
            "service_id": "BCA",
            "requestType": "SME"
        })
        headers = {
            "Content-Type": 'application/json',
            "Authorization": f'Bearer {public_key}'
        }
        response = requests.request('POST', url, headers=headers, data=payload)
        if response.status_code == 200:
            try:
                response_data = response.json()
                if response_data['details'] == None:
                    return 'Status Not Available'
                else:
                    return response_data['details']
            except json.JSONDecodeError:
                print("Invalid JSON data")
        else:
            return 'Status Not Available'

    def etisalat_get_plan():
        public_key = settings.MOBILENIG_PUBLIC_KEY
        url = "https://enterprise.mobilenig.com/api/services/packages"
        payload = json.dumps({
            "service_id": "BCB",
            "requestType": "SME"
        })
        headers = {
            "Content-Type": 'application/json',
            "Authorization": f'Bearer {public_key}'
        }
        response = requests.request('POST', url, headers=headers, data=payload)
        if response.status_code == 200:
            try:
                response_data = response.json()
                if response_data['details'] == None:
                    return 'Status Not Available'
                else:
                    return response_data['details']
            except json.JSONDecodeError:
                print("Invalid JSON data")
        else:
            return 'Status Not Available'

    def glo_get_plan():
        public_key = settings.MOBILENIG_PUBLIC_KEY
        url = "https://enterprise.mobilenig.com/api/services/packages"
        payload = json.dumps({
            "service_id": "BCC",
            "requestType": "SME"
        })
        headers = {
            "Content-Type": 'application/json',
            "Authorization": f'Bearer {public_key}'
        }
        response = requests.request('POST', url, headers=headers, data=payload)
        if response.status_code == 200:
            try:
                response_data = response.json()
                if response_data['details'] == None:
                    return 'Status Not Available'
                else:
                    return response_data['details']
            except json.JSONDecodeError:
                print("Invalid JSON data")
        else:
            return 'Status Not Available'

    def airtel_get_plan():
        public_key = settings.MOBILENIG_PUBLIC_KEY
        url = "https://enterprise.mobilenig.com/api/services/packages"
        payload = json.dumps({
            "service_id": "BCD",
            "requestType": "SME"
        })
        headers = {
            "Content-Type": 'application/json',
            "Authorization": f'Bearer {public_key}'
        }
        response = requests.request('POST', url, headers=headers, data=payload)
        if response.status_code == 200:
            try:
                response_data = response.json()
                if response_data['details'] == None:
                    return 'Status Not Available'
                else:
                    return response_data['details']
            except json.JSONDecodeError:
                print("Invalid JSON data")
        else:
            return 'Status Not Available'

class MNAirtimeRecharge:
    def mtn_recharge(request, topup_id):
        secret_key = settings.MOBILENIG_SECRET_KEY
        url = "https://enterprise.mobilenig.com/api/v2/services/"
        
        post = TopUp.objects.get(id=topup_id)
        payload = json.dumps({
            "service_id": "BAD",
            "trans_id": post.txn_id,
            "service_type": "PREMIUM",
            "phoneNumber": post.phone_number,
            "amount": post.amount
        })
        headers = {
            "Content-Type": 'application/json',
            "Authorization": f'Bearer {secret_key}'
        }
        response = requests.request('POST', url, headers=headers, data=payload)
        if response.status_code == 200:
            try:
                response_data = response.json()
                if response_data['details'] == None:
                    messages.error(request, f'Airtime Purchase Failed. Try Again Later')
                elif response_data['details'] == 'trans_id already exists.':
                    messages.error(request, f'Airtime Purchase Failed. Recurrent Transaction Discovered')
                elif response_data['message'] != 'success':
                    messages.error(request, f'Airtime Purchase Failed. Try Again Later')
                elif response_data['message'] == 'success':
                    post.status = 'Completed'
                    post.save()
                    post.account.user.balance -= post.amount
                    post.account.user.save()
                    data = Alert(amount=post.amount, balance=post.account.user.balance, user=post.account.user, topup=post, txn='Debit', how='Mobile', which='TOPUP')
                    data.detail = f'{data.topup.txn_id}/{data.how}/{data.which}'
                    data.save()
                    txn = Txn(account=post.account, topup=post, amount=post.amount)
                    txn.save()
                    if post.account.user.email_notification == True:
                        subject = 'Patridge Bank: Top Up Successful'
                        email_template_name = 'mail/topup_success.txt'
                        current_site = get_current_site(request)
                        context = {
                        'domain': current_site.domain,
                        "user": post.account.user,
                        "topup": post,
                        }
                        email = render_to_string(email_template_name, context)
                        try:
                            msg = EmailMultiAlternatives(subject, email, settings.EMAIL_HOST_USER, [post.account.user.email])
                            msg.send()
                        except BadHeaderError:
                            return redirect('Invalid header found.')
                    messages.success(request, f'Airtime Purchase Successful')
            except json.JSONDecodeError:
                print("Invalid JSON data")
        else:
            messages.error(request, f'Airtime Purchase Failed. Try Again Later')

    def etisalat_recharge(request, topup_id):
        secret_key = settings.MOBILENIG_SECRET_KEY
        url = "https://enterprise.mobilenig.com/api/v2/services/"
        
        post = TopUp.objects.get(id=topup_id)
        payload = json.dumps({
            "service_id": "BAC",
            "trans_id": post.txn_id,
            "service_type": "PREMIUM",
            "phoneNumber": post.phone_number,
            "amount": post.amount
        })
        headers = {
            "Content-Type": 'application/json',
            "Authorization": f'Bearer {secret_key}'
        }
        response = requests.request('POST', url, headers=headers, data=payload)
        if response.status_code == 200:
            try:
                response_data = response.json()
                if response_data['details'] == None:
                    messages.error(request, f'Airtime Purchase Failed. Try Again Later')
                elif response_data['details'] == 'trans_id already exists.':
                    messages.error(request, f'Airtime Purchase Failed. Recurrent Transaction Discovered')
                elif response_data['message'] != 'success':
                    messages.error(request, f'Airtime Purchase Failed. Try Again Later')
                elif response_data['message'] == 'success':
                    post.status = 'Completed'
                    post.save()
                    post.account.user.balance -= post.amount
                    post.account.user.save()
                    data = Alert(amount=post.amount, balance=post.account.user.balance, user=post.account.user, topup=post, txn='Debit', how='Mobile', which='TOPUP')
                    data.detail = f'{data.topup.txn_id}/{data.how}/{data.which}'
                    data.save()
                    txn = Txn(account=post.account, topup=post, amount=post.amount)
                    txn.save()
                    if post.account.user.email_notification == True:
                        subject = 'Patridge Bank: Top Up Successful'
                        email_template_name = 'mail/topup_success.txt'
                        current_site = get_current_site(request)
                        context = {
                        'domain': current_site.domain,
                        "user": post.account.user,
                        "topup": post,
                        }
                        email = render_to_string(email_template_name, context)
                        try:
                            msg = EmailMultiAlternatives(subject, email, settings.EMAIL_HOST_USER, [post.account.user.email])
                            msg.send()
                        except BadHeaderError:
                            return redirect('Invalid header found.')
                    messages.success(request, f'Airtime Purchase Successful')
            except json.JSONDecodeError:
                print("Invalid JSON data")
        else:
            messages.error(request, f'Airtime Purchase Failed. Try Again Later')

    def glo_recharge(request, topup_id):
        secret_key = settings.MOBILENIG_SECRET_KEY
        url = "https://enterprise.mobilenig.com/api/v2/services/"
        
        post = TopUp.objects.get(id=topup_id)
        payload = json.dumps({
            "service_id": "BAB",
            "trans_id": post.txn_id,
            "service_type": "PREMIUM",
            "phoneNumber": post.phone_number,
            "amount": post.amount
        })
        headers = {
            "Content-Type": 'application/json',
            "Authorization": f'Bearer {secret_key}'
        }
        response = requests.request('POST', url, headers=headers, data=payload)
        if response.status_code == 200:
            try:
                response_data = response.json()
                if response_data['details'] == None:
                    messages.error(request, f'Airtime Purchase Failed. Try Again Later')
                elif response_data['details'] == 'trans_id already exists.':
                    messages.error(request, f'Airtime Purchase Failed. Recurrent Transaction Discovered')
                elif response_data['message'] != 'success':
                    messages.error(request, f'Airtime Purchase Failed. Try Again Later')
                elif response_data['message'] == 'success':
                    post.status = 'Completed'
                    post.save()
                    post.account.user.balance -= post.amount
                    post.account.user.save()
                    data = Alert(amount=post.amount, balance=post.account.user.balance, user=post.account.user, topup=post, txn='Debit', how='Mobile', which='TOPUP')
                    data.detail = f'{data.topup.txn_id}/{data.how}/{data.which}'
                    data.save()
                    txn = Txn(account=post.account, topup=post, amount=post.amount)
                    txn.save()
                    if post.account.user.email_notification == True:
                        subject = 'Patridge Bank: Top Up Successful'
                        email_template_name = 'mail/topup_success.txt'
                        current_site = get_current_site(request)
                        context = {
                        'domain': current_site.domain,
                        "user": post.account.user,
                        "topup": post,
                        }
                        email = render_to_string(email_template_name, context)
                        try:
                            msg = EmailMultiAlternatives(subject, email, settings.EMAIL_HOST_USER, [post.account.user.email])
                            msg.send()
                        except BadHeaderError:
                            return redirect('Invalid header found.')
                    messages.success(request, f'Airtime Purchase Successful')
            except json.JSONDecodeError:
                print("Invalid JSON data")
        else:
            messages.error(request, f'Airtime Purchase Failed. Try Again Later')

    def airtel_recharge(request, topup_id):
        secret_key = settings.MOBILENIG_SECRET_KEY
        url = "https://enterprise.mobilenig.com/api/v2/services/"
        
        post = TopUp.objects.get(id=topup_id)
        payload = json.dumps({
            "service_id": "BAA",
            "trans_id": post.txn_id,
            "service_type": "PREMIUM",
            "phoneNumber": post.phone_number,
            "amount": post.amount
        })
        headers = {
            "Content-Type": 'application/json',
            "Authorization": f'Bearer {secret_key}'
        }
        response = requests.request('POST', url, headers=headers, data=payload)
        if response.status_code == 200:
            try:
                response_data = response.json()
                if response_data['details'] == None:
                    messages.error(request, f'Airtime Purchase Failed. Try Again Later')
                elif response_data['details'] == 'trans_id already exists.':
                    messages.error(request, f'Airtime Purchase Failed. Recurrent Transaction Discovered')
                elif response_data['message'] != 'success':
                    messages.error(request, f'Airtime Purchase Failed. Try Again Later')
                elif response_data['message'] == 'success':
                    post.status = 'Completed'
                    post.save()
                    post.account.user.balance -= post.amount
                    post.account.user.save()
                    data = Alert(amount=post.amount, balance=post.account.user.balance, user=post.account.user, topup=post, txn='Debit', how='Mobile', which='TOPUP')
                    data.detail = f'{data.topup.txn_id}/{data.how}/{data.which}'
                    data.save()
                    txn = Txn(account=post.account, topup=post, amount=post.amount)
                    txn.save()
                    if post.account.user.email_notification == True:
                        subject = 'Patridge Bank: Top Up Successful'
                        email_template_name = 'mail/topup_success.txt'
                        current_site = get_current_site(request)
                        context = {
                        'domain': current_site.domain,
                        "user": post.account.user,
                        "topup": post,
                        }
                        email = render_to_string(email_template_name, context)
                        try:
                            msg = EmailMultiAlternatives(subject, email, settings.EMAIL_HOST_USER, [post.account.user.email])
                            msg.send()
                        except BadHeaderError:
                            return redirect('Invalid header found.')
                    messages.success(request, f'Airtime Purchase Successful')
            except json.JSONDecodeError:
                print("Invalid JSON data")
        else:
            messages.error(request, f'Airtime Purchase Failed. Try Again Later')

class MNDataRecharge:
    def mtn_recharge(request, topup_id):
        secret_key = settings.MOBILENIG_SECRET_KEY
        url = "https://enterprise.mobilenig.com/api/v2/services/"
        
        post = TopUp.objects.get(id=topup_id)
        payload = json.dumps({
            "service_id": "BCA",
            "service_type": "SME",
            "beneficiary": post.phone_number,
            "trans_id": post.txn_id,
            "code": post.data.plan.product_code,
            "amount": post.amount
        })
        headers = {
            "Content-Type": 'application/json',
            "Authorization": f'Bearer {secret_key}'
        }
        response = requests.request('POST', url, headers=headers, data=payload)
        if response.status_code == 200:
            try:
                response_data = response.json()
                if response_data['details'] == None:
                    messages.error(request, f'Data Purchase Failed. Try Again Later')
                elif response_data['details'] == 'trans_id already exists.':
                    messages.error(request, f'Data Purchase Failed. Recurrent Transaction Discovered')
                elif response_data['message'] != 'success':
                    messages.error(request, f'Data Purchase Failed. Try Again Later')
                elif response_data['message'] == 'success':
                    post.status = 'Completed'
                    post.save()
                    post.account.user.balance -= post.amount
                    post.account.user.save()
                    data = Alert(amount=post.amount, balance=post.account.user.balance, user=post.account.user, topup=post, txn='Debit', how='Mobile', which='TOPUP')
                    data.detail = f'{data.topup.txn_id}/{data.how}/{data.which}'
                    data.save()
                    txn = Txn(account=post.account, topup=post, amount=post.amount)
                    txn.save()
                    if post.account.user.email_notification == True:
                        subject = 'Patridge Bank: Top Up Successful'
                        email_template_name = 'mail/topup_success.txt'
                        current_site = get_current_site(request)
                        context = {
                        'domain': current_site.domain,
                        "user": post.account.user,
                        "topup": post,
                        }
                        email = render_to_string(email_template_name, context)
                        try:
                            msg = EmailMultiAlternatives(subject, email, settings.EMAIL_HOST_USER, [post.account.user.email])
                            msg.send()
                        except BadHeaderError:
                            return redirect('Invalid header found.')
                    messages.success(request, f'Data Purchase Successful')
            except json.JSONDecodeError:
                print("Invalid JSON data")
        else:
            messages.error(request, f'Data Purchase Failed. Try Again Later')

    def etisalat_recharge(request, topup_id):
        secret_key = settings.MOBILENIG_SECRET_KEY
        url = "https://enterprise.mobilenig.com/api/v2/services/"
        
        post = TopUp.objects.get(id=topup_id)
        payload = json.dumps({
            "service_id": "BCB",
            "service_type": "SME",
            "beneficiary": post.phone_number,
            "trans_id": post.txn_id,
            "code": post.data.plan.product_code,
            "amount": post.amount
        })
        headers = {
            "Content-Type": 'application/json',
            "Authorization": f'Bearer {secret_key}'
        }
        response = requests.request('POST', url, headers=headers, data=payload)
        if response.status_code == 200:
            try:
                response_data = response.json()
                if response_data['details'] == None:
                    messages.error(request, f'Data Purchase Failed. Try Again Later')
                elif response_data['details'] == 'trans_id already exists.':
                    messages.error(request, f'Data Purchase Failed. Recurrent Transaction Discovered')
                elif response_data['message'] != 'success':
                    messages.error(request, f'Data Purchase Failed. Try Again Later')
                elif response_data['message'] == 'success':
                    post.status = 'Completed'
                    post.save()
                    post.account.user.balance -= post.amount
                    post.account.user.save()
                    data = Alert(amount=post.amount, balance=post.account.user.balance, user=post.account.user, topup=post, txn='Debit', how='Mobile', which='TOPUP')
                    data.detail = f'{data.topup.txn_id}/{data.how}/{data.which}'
                    data.save()
                    txn = Txn(account=post.account, topup=post, amount=post.amount)
                    txn.save()
                    if post.account.user.email_notification == True:
                        subject = 'Patridge Bank: Top Up Successful'
                        email_template_name = 'mail/topup_success.txt'
                        current_site = get_current_site(request)
                        context = {
                        'domain': current_site.domain,
                        "user": post.account.user,
                        "topup": post,
                        }
                        email = render_to_string(email_template_name, context)
                        try:
                            msg = EmailMultiAlternatives(subject, email, settings.EMAIL_HOST_USER, [post.account.user.email])
                            msg.send()
                        except BadHeaderError:
                            return redirect('Invalid header found.')
                    messages.success(request, f'Data Purchase Successful')
            except json.JSONDecodeError:
                print("Invalid JSON data")
        else:
            messages.error(request, f'Data Purchase Failed. Try Again Later')

    def glo_recharge(request, topup_id):
        secret_key = settings.MOBILENIG_SECRET_KEY
        url = "https://enterprise.mobilenig.com/api/v2/services/"
        
        post = TopUp.objects.get(id=topup_id)
        payload = json.dumps({
            "service_id": "BCC",
            "service_type": "SME",
            "beneficiary": post.phone_number,
            "trans_id": post.txn_id,
            "code": post.data.plan.product_code,
            "amount": post.amount
        })
        headers = {
            "Content-Type": 'application/json',
            "Authorization": f'Bearer {secret_key}'
        }
        response = requests.request('POST', url, headers=headers, data=payload)
        if response.status_code == 200:
            try:
                response_data = response.json()
                if response_data['details'] == None:
                    messages.error(request, f'Data Purchase Failed. Try Again Later')
                elif response_data['details'] == 'trans_id already exists.':
                    messages.error(request, f'Data Purchase Failed. Recurrent Transaction Discovered')
                elif response_data['message'] != 'success':
                    messages.error(request, f'Data Purchase Failed. Try Again Later')
                elif response_data['message'] == 'success':
                    post.status = 'Completed'
                    post.save()
                    post.account.user.balance -= post.amount
                    post.account.user.save()
                    data = Alert(amount=post.amount, balance=post.account.user.balance, user=post.account.user, topup=post, txn='Debit', how='Mobile', which='TOPUP')
                    data.detail = f'{data.topup.txn_id}/{data.how}/{data.which}'
                    data.save()
                    txn = Txn(account=post.account, topup=post, amount=post.amount)
                    txn.save()
                    if post.account.user.email_notification == True:
                        subject = 'Patridge Bank: Top Up Successful'
                        email_template_name = 'mail/topup_success.txt'
                        current_site = get_current_site(request)
                        context = {
                        'domain': current_site.domain,
                        "user": post.account.user,
                        "topup": post,
                        }
                        email = render_to_string(email_template_name, context)
                        try:
                            msg = EmailMultiAlternatives(subject, email, settings.EMAIL_HOST_USER, [post.account.user.email])
                            msg.send()
                        except BadHeaderError:
                            return redirect('Invalid header found.')
                    messages.success(request, f'Data Purchase Successful')
            except json.JSONDecodeError:
                print("Invalid JSON data")
        else:
            messages.error(request, f'Data Purchase Failed. Try Again Later')

    def airtel_recharge(request, topup_id):
        secret_key = settings.MOBILENIG_SECRET_KEY
        url = "https://enterprise.mobilenig.com/api/v2/services/"
        
        post = TopUp.objects.get(id=topup_id)
        payload = json.dumps({
            "service_id": "BCD",
            "service_type": "SME",
            "beneficiary": post.phone_number,
            "trans_id": post.txn_id,
            "code": post.data.plan.product_code,
            "amount": post.amount
        })
        headers = {
            "Content-Type": 'application/json',
            "Authorization": f'Bearer {secret_key}'
        }
        response = requests.request('POST', url, headers=headers, data=payload)
        if response.status_code == 200:
            try:
                response_data = response.json()
                if response_data['details'] == None:
                    messages.error(request, f'Data Purchase Failed. Try Again Later')
                elif response_data['details'] == 'trans_id already exists.':
                    messages.error(request, f'Data Purchase Failed. Recurrent Transaction Discovered')
                elif response_data['message'] != 'success':
                    messages.error(request, f'Data Purchase Failed. Try Again Later')
                elif response_data['message'] == 'success':
                    post.status = 'Completed'
                    post.save()
                    post.account.user.balance -= post.amount
                    post.account.user.save()
                    data = Alert(amount=post.amount, balance=post.account.user.balance, user=post.account.user, topup=post, txn='Debit', how='Mobile', which='TOPUP')
                    data.detail = f'{data.topup.txn_id}/{data.how}/{data.which}'
                    data.save()
                    txn = Txn(account=post.account, topup=post, amount=post.amount)
                    txn.save()
                    if post.account.user.email_notification == True:
                        subject = 'Patridge Bank: Top Up Successful'
                        email_template_name = 'mail/topup_success.txt'
                        current_site = get_current_site(request)
                        context = {
                        'domain': current_site.domain,
                        "user": post.account.user,
                        "topup": post,
                        }
                        email = render_to_string(email_template_name, context)
                        try:
                            msg = EmailMultiAlternatives(subject, email, settings.EMAIL_HOST_USER, [post.account.user.email])
                            msg.send()
                        except BadHeaderError:
                            return redirect('Invalid header found.')
                    messages.success(request, f'Data Purchase Successful')
            except json.JSONDecodeError:
                print("Invalid JSON data")
        else:
            messages.error(request, f'Data Purchase Failed. Try Again Later')

class MNCable:
    def gotv_get_package():
        public_key = settings.MOBILENIG_PUBLIC_KEY
        url = "https://enterprise.mobilenig.com/api/v2/services/packages"
        payload = json.dumps({
            "service_id": "AKA",
        })
        headers = {
            "Content-Type": 'application/json',
            "Authorization": f'Bearer {public_key}'
        }
        response = requests.request('POST', url, headers=headers, data=payload)
        if response.status_code == 200:
            try:
                response_data = response.json()
                if response_data['details'] == None:
                    return 'Status Not Available'
                else:
                    return response_data['details']
            except json.JSONDecodeError:
                print("Invalid JSON data")
        else:
            return 'Status Not Available'

    def gotv_get_details(pk):
        public_key = settings.MOBILENIG_PUBLIC_KEY
        url = "https://enterprise.mobilenig.com/api/v2/services/proxy"

        post = Bill.objects.get(id=pk)
        payload = json.dumps({
            "service_id": "AKA",
            "customerAccountId": post.cable.card_number
        })
        headers = {
            "Content-Type": 'application/json',
            "Authorization": f'Bearer {public_key}'
        }
        response = requests.request('POST', url, headers=headers, data=payload)
        if response.status_code == 200:
            try:
                response_data = response.json()
                if response_data['details'] == None:
                    return 'Error'
                elif response_data['message'] != 'success':
                    return 'Error'
                elif response_data['message'] == 'success':
                    return response_data['details']
            except json.JSONDecodeError:
                print("Invalid JSON data")
        else:
            return 'Error'

    def gotv_recharge(request, pk):
        secret_key = settings.MOBILENIG_SECRET_KEY
        url = "https://enterprise.mobilenig.com/api/v2/services/"
        
        post = Bill.objects.get(id=pk)
        payload = json.dumps({
            "service_id": "AKA",
            "trans_id" : post.txn_id,
            "productCode" : post.cable.plan.product_code,
            "customerNumber" : post.cable.customer_number, 
            "smartcardNumber" : post.cable.card_number, 
            "customerName" : post.cable.customer_name,
            "amount" : post.amount
        })
        headers = {
            "Content-Type": 'application/json',
            "Authorization": f'Bearer {secret_key}'
        }
        response = requests.request('POST', url, headers=headers, data=payload)
        if response.status_code == 200:
            try:
                response_data = response.json()
                if response_data['details'] == None:
                    messages.error(request, f'GOTV Recharge Failed. Try Again Later')
                elif response_data['details'] == 'trans_id already exists.':
                    messages.error(request, f'GOTV Recharge Failed. Recurrent Transaction Discovered')
                elif response_data['message'] != 'success':
                    print(response_data)
                    messages.error(request, f'GOTV Recharge Failed. Try Again Later')
                elif response_data['message'] == 'success':
                    post.status = 'Completed'
                    post.save()
                    post.account.user.balance -= post.amount
                    post.account.user.save()
                    data = Alert(amount=post.amount, balance=post.account.user.balance, user=post.account.user, bill=post, txn='Debit', how='Mobile', which='BILL')
                    data.detail = f'{data.bill.txn_id}/{data.how}/{data.which}'
                    data.save()
                    txn = Txn(account=post.account, bill=post, amount=post.amount)
                    txn.save()
                    result = response_data['details']
                    post.cable.exchange_reference = result['details']['exchangeReference']
                    post.cable.customercare_referenceid = result['details']['customerCareReferenceId']
                    post.cable.audit_referencenumber = result['details']['auditReferenceNumber']
                    post.cable.save()
                    if post.account.user.email_notification == True:
                        subject = 'Patridge Bank: Bill Payment Successful'
                        email_template_name = 'mail/payment_success.txt'
                        current_site = get_current_site(request)
                        context = {
                        'domain': current_site.domain,
                        "user": post.account.user,
                        "bill": post,
                        }
                        email = render_to_string(email_template_name, context)
                        try:
                            msg = EmailMultiAlternatives(subject, email, settings.EMAIL_HOST_USER, [post.account.user.email])
                            msg.send()
                        except BadHeaderError:
                            return redirect('Invalid header found.')
                    messages.success(request, f'GOTV Recharge Successful')
            except json.JSONDecodeError:
                print("Invalid JSON data")
        else:
            messages.error(request, f'GOTV Recharge Failed. Try Again Later')

    def dstv_get_package():
        public_key = settings.MOBILENIG_PUBLIC_KEY
        url = "https://enterprise.mobilenig.com/api/v2/services/packages"
        payload = json.dumps({
            "service_id": "AKC",
        })
        headers = {
            "Content-Type": 'application/json',
            "Authorization": f'Bearer {public_key}'
        }
        response = requests.request('POST', url, headers=headers, data=payload)
        if response.status_code == 200:
            try:
                response_data = response.json()
                if response_data['details'] == None:
                    return 'Status Not Available'
                else:
                    return response_data['details']
            except json.JSONDecodeError:
                print("Invalid JSON data")
        else:
            return 'Status Not Available'

    def dstv_get_details(pk):
        public_key = settings.MOBILENIG_PUBLIC_KEY
        url = "https://enterprise.mobilenig.com/api/v2/services/proxy"

        post = Bill.objects.get(id=pk)
        payload = json.dumps({
            "service_id": "AKC",
            "customerAccountId": post.cable.card_number
        })
        headers = {
            "Content-Type": 'application/json',
            "Authorization": f'Bearer {public_key}'
        }
        response = requests.request('POST', url, headers=headers, data=payload)
        if response.status_code == 200:
            try:
                response_data = response.json()
                if response_data['details'] == None:
                    return 'Error'
                elif response_data['message'] != 'success':
                    return 'Error'
                elif response_data['message'] == 'success':
                    return response_data['details']
            except json.JSONDecodeError:
                print("Invalid JSON data")
        else:
            return 'Error'

    def dstv_recharge(request, pk):
        secret_key = settings.MOBILENIG_SECRET_KEY
        url = "https://enterprise.mobilenig.com/api/v2/services/"
        
        post = Bill.objects.get(id=pk)
        payload = json.dumps({
            "service_id": "AKC",
            "trans_id" : post.txn_id,
            "productCode" : post.cable.plan.product_code,
            "customerNumber" : post.cable.customer_number, 
            "smartcardNumber" : post.cable.card_number, 
            "customerName" : post.cable.customer_name,
            "amount" : post.amount
        })
        headers = {
            "Content-Type": 'application/json',
            "Authorization": f'Bearer {secret_key}'
        }
        response = requests.request('POST', url, headers=headers, data=payload)
        if response.status_code == 200:
            try:
                response_data = response.json()
                if response_data['details'] == None:
                    messages.error(request, f'DSTV Recharge Failed. Try Again Later')
                elif response_data['details'] == 'trans_id already exists.':
                    messages.error(request, f'DSTV Recharge Failed. Recurrent Transaction Discovered')
                elif response_data['message'] != 'success':
                    messages.error(request, f'DSTV Recharge Failed. Try Again Later')
                elif response_data['message'] == 'success':
                    post.status = 'Completed'
                    post.save()
                    post.account.user.balance -= post.amount
                    post.account.user.save()
                    data = Alert(amount=post.amount, balance=post.account.user.balance, user=post.account.user, bill=post, txn='Debit', how='Mobile', which='BILL')
                    data.detail = f'{data.bill.txn_id}/{data.how}/{data.which}'
                    data.save()
                    txn = Txn(account=post.account, bill=post, amount=post.amount)
                    txn.save()
                    result = response_data['details']
                    post.cable.exchange_reference = result['details']['exchangeReference']
                    post.cable.customercare_referenceid = result['details']['customerCareReferenceId']
                    post.cable.audit_referencenumber = result['details']['auditReferenceNumber']
                    post.cable.save()
                    if post.account.user.email_notification == True:
                        subject = 'Patridge Bank: Bill Payment Successful'
                        email_template_name = 'mail/payment_success.txt'
                        current_site = get_current_site(request)
                        context = {
                        'domain': current_site.domain,
                        "user": post.account.user,
                        "bill": post,
                        }
                        email = render_to_string(email_template_name, context)
                        try:
                            msg = EmailMultiAlternatives(subject, email, settings.EMAIL_HOST_USER, [post.account.user.email])
                            msg.send()
                        except BadHeaderError:
                            return redirect('Invalid header found.')
                    messages.success(request, f'DSTV Recharge Successful')
            except json.JSONDecodeError:
                print("Invalid JSON data")
        else:
            messages.error(request, f'DSTV Recharge Failed. Try Again Later')

    def startimes_get_package():
        public_key = settings.MOBILENIG_PUBLIC_KEY
        url = "https://enterprise.mobilenig.com/api/v2/services/packages"
        payload = json.dumps({
            "service_id": "AKB",
        })
        headers = {
            "Content-Type": 'application/json',
            "Authorization": f'Bearer {public_key}'
        }
        response = requests.request('POST', url, headers=headers, data=payload)
        if response.status_code == 200:
            try:
                response_data = response.json()
                if response_data['details'] == None:
                    return 'Status Not Available'
                else:
                    return response_data['details']
            except json.JSONDecodeError:
                print("Invalid JSON data")
        else:
            return 'Status Not Available'

    def startimes_get_details(pk):
        public_key = settings.MOBILENIG_PUBLIC_KEY
        url = "https://enterprise.mobilenig.com/api/v2/services/proxy"

        post = Bill.objects.get(id=pk)
        payload = json.dumps({
            "service_id": "AKB",
            "customerAccountId": post.cable.card_number
        })
        headers = {
            "Content-Type": 'application/json',
            "Authorization": f'Bearer {public_key}'
        }
        response = requests.request('POST', url, headers=headers, data=payload)
        if response.status_code == 200:
            try:
                response_data = response.json()
                if response_data['details'] == None:
                    return 'Error'
                elif response_data['message'] != 'success':
                    return 'Error'
                elif response_data['message'] == 'success':
                    return response_data['details']
            except json.JSONDecodeError:
                print("Invalid JSON data")
        else:
            return 'Error'

    def startimes_recharge(request, pk):
        secret_key = settings.MOBILENIG_SECRET_KEY
        url = "https://enterprise.mobilenig.com/api/v2/services/"
        
        post = Bill.objects.get(id=pk)
        payload = json.dumps({
            "service_id": "AKB",
            "trans_id" : post.txn_id,
            "productCode" : post.cable.plan.product_code,
            "customerNumber" : post.cable.customer_number, 
            "smartcardNumber" : post.cable.card_number,
            "amount" : post.amount
        })
        headers = {
            "Content-Type": 'application/json',
            "Authorization": f'Bearer {secret_key}'
        }
        response = requests.request('POST', url, headers=headers, data=payload)
        if response.status_code == 200:
            try:
                response_data = response.json()
                if response_data['details'] == None:
                    messages.error(request, f'Startimes Recharge Failed. Try Again Later')
                elif response_data['details'] == 'trans_id already exists.':
                    messages.error(request, f'Startimes Recharge Failed. Recurrent Transaction Discovered')
                elif response_data['message'] != 'success':
                    messages.error(request, f'Startimes Recharge Failed. Try Again Later')
                elif response_data['message'] == 'success':
                    post.status = 'Completed'
                    post.save()
                    post.account.user.balance -= post.amount
                    post.account.user.save()
                    data = Alert(amount=post.amount, balance=post.account.user.balance, user=post.account.user, bill=post, txn='Debit', how='Mobile', which='BILL')
                    data.detail = f'{data.bill.txn_id}/{data.how}/{data.which}'
                    data.save()
                    txn = Txn(account=post.account, bill=post, amount=post.amount)
                    txn.save()
                    result = response_data['details']
                    post.cable.exchange_reference = result['details']['exchangeReference']
                    post.cable.save()
                    if post.account.user.email_notification == True:
                        subject = 'Patridge Bank: Bill Payment Successful'
                        email_template_name = 'mail/payment_success.txt'
                        current_site = get_current_site(request)
                        context = {
                        'domain': current_site.domain,
                        "user": post.account.user,
                        "bill": post,
                        }
                        email = render_to_string(email_template_name, context)
                        try:
                            msg = EmailMultiAlternatives(subject, email, settings.EMAIL_HOST_USER, [post.account.user.email])
                            msg.send()
                        except BadHeaderError:
                            return redirect('Invalid header found.')
                    messages.success(request, f'Startimes Recharge Successful')
            except json.JSONDecodeError:
                print("Invalid JSON data")
        else:
            messages.error(request, f'Startimes Recharge Failed. Try Again Later')

class MNElectricity:
    def eko_get_details(pk):
        public_key = settings.MOBILENIG_PUBLIC_KEY
        url = "https://enterprise.mobilenig.com/api/v2/services/proxy"

        post = Bill.objects.get(id=pk)
        payload = json.dumps({
            "service_id": "ANA",
            "customerAccountId": post.electricity.meter_number
        })
        headers = {
            "Content-Type": 'application/json',
            "Authorization": f'Bearer {public_key}'
        }
        response = requests.request('POST', url, headers=headers, data=payload)
        if response.status_code == 200:
            try:
                response_data = response.json()
                if response_data['details'] == None:
                    return 'Error'
                elif response_data['message'] != 'success':
                    return 'Error'
                elif response_data['message'] == 'success':
                    return response_data['details']
            except json.JSONDecodeError:
                print("Invalid JSON data")
        else:
            return 'Error'

    def eko_recharge(request, pk):
        secret_key = settings.MOBILENIG_SECRET_KEY
        url = "https://enterprise.mobilenig.com/api/v2/services/"
        
        post = Bill.objects.get(id=pk)
        payload = json.dumps({
            "service_id": "ANA",
            "trans_id": post.txn_id,
            "customerAddress": post.electricity.customer_address,
            "customerDistrict": post.electricity.customer_district,
            "customerName": post.electricity.customer_name,
            "meterNumber": post.electricity.meter_number,
            "amount": post.amount
        })
        headers = {
            "Content-Type": 'application/json',
            "Authorization": f'Bearer {secret_key}'
        }
        response = requests.request('POST', url, headers=headers, data=payload)
        if response.status_code == 200:
            try:
                response_data = response.json()
                if response_data['details'] == None:
                    messages.error(request, f'Electricity Bill Payment Failed. Try Again Later')
                elif response_data['details'] == 'trans_id already exists.':
                    messages.error(request, f'Electricity Bill Payment Failed. Recurrent Transaction Discovered')
                elif response_data['message'] != 'success':
                    messages.error(request, f'Electricity Bill Payment Failed. Try Again Later')
                elif response_data['message'] == 'success':
                    post.status = 'Completed'
                    post.save()
                    post.account.user.balance -= post.amount
                    post.account.user.save()
                    data = Alert(amount=post.amount, balance=post.account.user.balance, user=post.account.user, bill=post, txn='Debit', how='Mobile', which='BILL')
                    data.detail = f'{data.bill.txn_id}/{data.how}/{data.which}'
                    data.save()
                    txn = Txn(account=post.account, bill=post, amount=post.amount)
                    txn.save()
                    result = response_data['details']
                    post.electricity.bsst_tokenvalue = result['details']['bsstTokenValue']
                    post.electricity.standard_tokenvalue = result['details']['standardTokenValue']
                    post.electricity.utility_name = result['details']['utilityName']
                    post.electricity.exchange_reference = result['details']['exchangeReference']
                    post.electricity.save()
                    if post.account.user.email_notification == True:
                        subject = 'Patridge Bank: Bill Payment Successful'
                        email_template_name = 'mail/payment_success.txt'
                        current_site = get_current_site(request)
                        context = {
                        'domain': current_site.domain,
                        "user": post.account.user,
                        "bill": post,
                        }
                        email = render_to_string(email_template_name, context)
                        try:
                            msg = EmailMultiAlternatives(subject, email, settings.EMAIL_HOST_USER, [post.account.user.email])
                            msg.send()
                        except BadHeaderError:
                            return redirect('Invalid header found.')
                    messages.success(request, f'Electricity Bill Payment Successful')
            except json.JSONDecodeError:
                print("Invalid JSON data")
        else:
            messages.error(request, f'Electricity Bill Payment Failed. Try Again Later')

    def abuja_get_details(pk):
        public_key = settings.MOBILENIG_PUBLIC_KEY
        url = "https://enterprise.mobilenig.com/api/v2/services/proxy"

        post = Bill.objects.get(id=pk)
        payload = json.dumps({
            "service_id": "AHB",
            "customerAccountId": post.electricity.meter_number
        })
        headers = {
            "Content-Type": 'application/json',
            "Authorization": f'Bearer {public_key}'
        }
        response = requests.request('POST', url, headers=headers, data=payload)
        if response.status_code == 200:
            try:
                response_data = response.json()
                if response_data['details'] == None:
                    return 'Error'
                elif response_data['message'] != 'success':
                    return 'Error'
                elif response_data['message'] == 'success':
                    return response_data['details']
            except json.JSONDecodeError:
                print("Invalid JSON data")
        else:
            return 'Error'

    def abuja_recharge(request, pk):
        secret_key = settings.MOBILENIG_SECRET_KEY
        url = "https://enterprise.mobilenig.com/api/v2/services/"
        
        post = Bill.objects.get(id=pk)
        payload = json.dumps({
            "service_id": "AHB",
            "trans_id": post.txn_id,
            "customerReference": post.electricity.customer_reference,
            "amount": post.amount,
            "customerName": post.electricity.customer_name,
            "customerAddress": post.electricity.customer_address
        })
        headers = {
            "Content-Type": 'application/json',
            "Authorization": f'Bearer {secret_key}'
        }
        response = requests.request('POST', url, headers=headers, data=payload)
        if response.status_code == 200:
            try:
                response_data = response.json()
                if response_data['details'] == None:
                    messages.error(request, f'Electricity Bill Payment Failed. Try Again Later')
                elif response_data['details'] == 'trans_id already exists.':
                    messages.error(request, f'Electricity Bill Payment Failed. Recurrent Transaction Discovered')
                elif response_data['message'] != 'success':
                    messages.error(request, f'Electricity Bill Payment Failed. Try Again Later')
                elif response_data['message'] == 'success':
                    post.status = 'Completed'
                    post.save()
                    post.account.user.balance -= post.amount
                    post.account.user.save()
                    data = Alert(amount=post.amount, balance=post.account.user.balance, user=post.account.user, bill=post, txn='Debit', how='Mobile', which='BILL')
                    data.detail = f'{data.bill.txn_id}/{data.how}/{data.which}'
                    data.save()
                    txn = Txn(account=post.account, bill=post, amount=post.amount)
                    txn.save()
                    result = response_data['details']
                    post.electricity.token = result['details']['token']
                    post.electricity.receipt_number = result['details']['receiptNumber']
                    post.electricity.exchange_reference = result['details']['reference']
                    post.electricity.save()
                    if post.account.user.email_notification == True:
                        subject = 'Patridge Bank: Bill Payment Successful'
                        email_template_name = 'mail/payment_success.txt'
                        current_site = get_current_site(request)
                        context = {
                        'domain': current_site.domain,
                        "user": post.account.user,
                        "bill": post,
                        }
                        email = render_to_string(email_template_name, context)
                        try:
                            msg = EmailMultiAlternatives(subject, email, settings.EMAIL_HOST_USER, [post.account.user.email])
                            msg.send()
                        except BadHeaderError:
                            return redirect('Invalid header found.')
                    messages.success(request, f'Electricity Bill Payment Successful')
            except json.JSONDecodeError:
                print("Invalid JSON data")
        else:
            messages.error(request, f'Electricity Bill Payment Failed. Try Again Later')

    def kaduna_get_details(pk):
        public_key = settings.MOBILENIG_PUBLIC_KEY
        url = "https://enterprise.mobilenig.com/api/v2/services/proxy"

        post = Bill.objects.get(id=pk)
        payload = json.dumps({
            "service_id": "AGB",
            "customerAccountId": post.electricity.meter_number
        })
        headers = {
            "Content-Type": 'application/json',
            "Authorization": f'Bearer {public_key}'
        }
        response = requests.request('POST', url, headers=headers, data=payload)
        if response.status_code == 200:
            try:
                response_data = response.json()
                if response_data['details'] == None:
                    return 'Error'
                elif response_data['message'] != 'success':
                    return 'Error'
                elif response_data['message'] == 'success':
                    return response_data['details']
            except json.JSONDecodeError:
                print("Invalid JSON data")
        else:
            return 'Error'

    def kaduna_recharge(request, pk):
        secret_key = settings.MOBILENIG_SECRET_KEY
        url = "https://enterprise.mobilenig.com/api/v2/services/"
        
        post = Bill.objects.get(id=pk)
        payload = json.dumps({
            "service_id": "AGB",
            "trans_id": post.txn_id,
            "meterNumber": post.electricity.meter_number,
            "amount": post.amount,
            "customerName": post.electricity.customer_name,
            "customerAddress": post.electricity.customer_address,
            "tariff": "R2S",
            "customerMobileNumber": post.electricity.phone_number
        })
        headers = {
            "Content-Type": 'application/json',
            "Authorization": f'Bearer {secret_key}'
        }
        response = requests.request('POST', url, headers=headers, data=payload)
        if response.status_code == 200:
            try:
                response_data = response.json()
                if response_data['details'] == None:
                    messages.error(request, f'Electricity Bill Payment Failed. Try Again Later')
                elif response_data['details'] == 'trans_id already exists.':
                    messages.error(request, f'Electricity Bill Payment Failed. Recurrent Transaction Discovered')
                elif response_data['message'] != 'success':
                    messages.error(request, f'Electricity Bill Payment Failed. Try Again Later')
                elif response_data['message'] == 'success':
                    post.status = 'Completed'
                    post.save()
                    post.account.user.balance -= post.amount
                    post.account.user.save()
                    data = Alert(amount=post.amount, balance=post.account.user.balance, user=post.account.user, bill=post, txn='Debit', how='Mobile', which='BILL')
                    data.detail = f'{data.bill.txn_id}/{data.how}/{data.which}'
                    data.save()
                    txn = Txn(account=post.account, bill=post, amount=post.amount)
                    txn.save()
                    result = response_data['details']
                    post.electricity.token = result['details']['token']
                    post.electricity.unit = result['details']['units']
                    post.electricity.receipt_number = result['details']['receiptNumber']
                    post.electricity.exchange_reference = result['details']['discoExchangeReference']
                    post.electricity.save()
                    if post.account.user.email_notification == True:
                        subject = 'Patridge Bank: Bill Payment Successful'
                        email_template_name = 'mail/payment_success.txt'
                        current_site = get_current_site(request)
                        context = {
                        'domain': current_site.domain,
                        "user": post.account.user,
                        "bill": post,
                        }
                        email = render_to_string(email_template_name, context)
                        try:
                            msg = EmailMultiAlternatives(subject, email, settings.EMAIL_HOST_USER, [post.account.user.email])
                            msg.send()
                        except BadHeaderError:
                            return redirect('Invalid header found.')
                    messages.success(request, f'Electricity Bill Payment Successful')
            except json.JSONDecodeError:
                print("Invalid JSON data")
        else:
            messages.error(request, f'Electricity Bill Payment Failed. Try Again Later')

    def ibadan_get_details(pk):
        public_key = settings.MOBILENIG_PUBLIC_KEY
        url = "https://enterprise.mobilenig.com/api/v2/services/proxy"

        post = Bill.objects.get(id=pk)
        payload = json.dumps({
            "service_id": "AEA",
            "customerAccountId": post.electricity.meter_number
        })
        headers = {
            "Content-Type": 'application/json',
            "Authorization": f'Bearer {public_key}'
        }
        response = requests.request('POST', url, headers=headers, data=payload)
        if response.status_code == 200:
            try:
                response_data = response.json()
                print(response_data)
                if response_data['details'] == None:
                    return 'Error'
                elif response_data['message'] != 'success':
                    return 'Error'
                elif response_data['message'] == 'success':
                    return response_data['details']
            except json.JSONDecodeError:
                print("Invalid JSON data")
        else:
            return 'Error'

    def ibadan_recharge(request, pk):
        secret_key = settings.MOBILENIG_SECRET_KEY
        url = "https://enterprise.mobilenig.com/api/v2/services/"
        
        post = Bill.objects.get(id=pk)
        payload = json.dumps({
            "service_id": "AEA",
            "trans_id": post.txn_id,
            "customerName": post.electricity.customer_name,
            "customerReference": post.electricity.meter_number,
            "customerType": "PREPAID",
            "thirdPartyCode": "ONLI",
            "serviceBand": "D8H",
            "amount": post.amount
        })
        headers = {
            "Content-Type": 'application/json',
            "Authorization": f'Bearer {secret_key}'
        }
        response = requests.request('POST', url, headers=headers, data=payload)
        if response.status_code == 200:
            try:
                response_data = response.json()
                if response_data['details'] == None:
                    messages.error(request, f'Electricity Bill Payment Failed. Try Again Later')
                elif response_data['details'] == 'trans_id already exists.':
                    messages.error(request, f'Electricity Bill Payment Failed. Recurrent Transaction Discovered')
                elif response_data['message'] != 'success':
                    messages.error(request, f'Electricity Bill Payment Failed. Try Again Later')
                elif response_data['message'] == 'success':
                    post.status = 'Completed'
                    post.save()
                    post.account.user.balance -= post.amount
                    post.account.user.save()
                    data = Alert(amount=post.amount, balance=post.account.user.balance, user=post.account.user, bill=post, txn='Debit', how='Mobile', which='BILL')
                    data.detail = f'{data.bill.txn_id}/{data.how}/{data.which}'
                    data.save()
                    txn = Txn(account=post.account, bill=post, amount=post.amount)
                    txn.save()
                    result = response_data['details']
                    post.electricity.tariff_code = result['details']['tariff']
                    post.electricity.token = result['details']['token']
                    post.electricity.bsst_tokenvalue = result['details']['resetToken']
                    post.electricity.customer_reference = result['details']['customerReference']
                    post.electricity.exchange_reference = result['details']['exchangeReference']
                    post.electricity.save()
                    if post.account.user.email_notification == True:
                        subject = 'Patridge Bank: Bill Payment Successful'
                        email_template_name = 'mail/payment_success.txt'
                        current_site = get_current_site(request)
                        context = {
                        'domain': current_site.domain,
                        "user": post.account.user,
                        "bill": post,
                        }
                        email = render_to_string(email_template_name, context)
                        try:
                            msg = EmailMultiAlternatives(subject, email, settings.EMAIL_HOST_USER, [post.account.user.email])
                            msg.send()
                        except BadHeaderError:
                            return redirect('Invalid header found.')
                    messages.success(request, f'Electricity Bill Payment Successful')
            except json.JSONDecodeError:
                print("Invalid JSON data")
        else:
            messages.error(request, f'Electricity Bill Payment Failed. Try Again Later')
