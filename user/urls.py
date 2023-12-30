from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('customer/login/', CustomerLoginView, name='customer_login'),
    path('customer/register/', CustomerRegisterView, name='customer_register'),
    path('customer/register/continue/<int:pk>/', CustomerCreateAccountView, name='customer_create'),
    path('customer/register/pin/<int:pk>/', AddPinView, name='addpin'),
    path('customer/logout/', CustomerLogOutView, name='customer_logout'),
    path('customer/password/reset/', CustomerPasswordResetRequestView, name='customer_password_reset'),
    path('customer/password/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="general/password_confirm.html", success_url="/portal/customer/password/reset/done/"), name='customer_password_confirm'),
    path('customer/password/reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='customer/password_reset_complete.html'), name='customer_password_reset_complete'),
    path('customer/password_change/', auth_views.PasswordChangeView.as_view(template_name='customer/password_change.html', success_url='/portal/customer/password_change/done/'), name='customer_password_change'),
    path('customer/password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='customer/password_change_done.html'), name='customer_password_change_done'),
    
    path('account/activate/(<uidb64>[0-9A-Za-z_\-]+)/(<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', ActivateAccountView, name='activate'),
    path('term/', TermView, name='term'),
    path('privacy/', PrivacyView, name='privacy'),
    
    path('staff/login/', StaffLoginView, name='staff_login'),
    path('staff/register/', StaffRegisterView, name='staff_register'),
    path('staff/register/continue/<int:pk>/', StaffCreateAccountView, name='staff_create'),
    path('staff/logout/', StaffLogOutView, name='staff_logout'),
    path('staff/password/reset/', StaffPasswordResetRequestView, name='staff_password_reset'),
    path('staff/password/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="general/password_confirm.html", success_url="/portal/staff/password/reset/done/"), name='staff_password_confirm'),
    path('staff/password/reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='staff/password_reset_complete.html'), name='staff_password_reset_complete'),
    path('staff/password_change/', auth_views.PasswordChangeView.as_view(template_name='staff/password_change.html', success_url='/portal/staff/password_change/done/'), name='staff_password_change'),
    path('staff/password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='staff/password_change_done.html'), name='staff_password_change_done'),
]
