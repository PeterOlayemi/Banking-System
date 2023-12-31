from django.urls import path
from .views import *

urlpatterns = [
    path('dashboard/', CustomerHomeView, name='customer_home'),
    path('more/alert/', MoreAlertView, name='morealert'),
    path('detail/alert/<int:pk>/', DetailAlertView, name='detailalert'),
    path('more/exchange/', MoreExchangeView, name='moreexchange'),
    path('more/news/', MoreNewsView, name='morenews'),
    path('detail/news/<int:pk>/', DetailNewsView, name='detailnews'),
    path('more/', MoreView, name='more'),
    path('transfer/', TransferView, name='transfer'),
    path('more/transfer/', MoreTransferView, name='moretransfer'),
    path('detail/transfer/<int:pk>/', DetailTransferView, name='detailtransfer'),
    path('local/transfer/', LocalTransferView, name='localtransfer'),
    path('repeat/transfer/<int:pk>/', RepeatTransferView, name='repeattransfer'),
    path('confirm/transfer/<int:pk>/', ConfirmTransferView, name='confirmtransfer'),
    path('validate/transfer/<int:pk>/', ValidateTransferView, name='validatetransfer'),
    path('pay/', BillView, name='bill'),
    path('more/saved/', MoreBillSavedView, name='moresaved'),
    path('more/bill/', MoreBillView, name='morebill'),
    path('new/pay/', NewBillView, name='newbill'),
    path('detail/bill/<int:pk>/', DetailBillView, name='detailbill'),
    path('cable/get_plans_for_service/', CablePlansForServiceView),
    path('cable/pay/', CablePaymentView, name='cable'),
    path('electricity/pay/', ElectricityPaymentView, name='electricity'),
    path('repeat/electricity/<int:pk>/', RepeatElectricityView, name='repeatelectricity'),
    path('confirm/bill/<int:pk>/', ConfirmBillView, name='confirmbill'),
    path('validate/bill/<int:pk>/', ValidateBillView, name='validatebill'),
    path('topup/', TopUpView, name='topup'),
    path('new/topup/', NewTopUpView, name='newtop'),
    path('detail/topup/<int:pk>/', DetailTopView, name='detailtop'),
    path('more/saved/topup/', MoreTopSavedView, name='moresavedtop'),
    path('more/topup/', MoreTopView, name='moretop'),
    path('airtime/pay/', AirtimeView, name='airtime'),
    path('repeat/airtime/<int:pk>/', RepeatAirtimeView, name='repeatairtime'),
    path('data/get_plans_for_service/', DataPlansForServiceView),
    path('data/pay/', DataView, name='data'),
    path('repeat/data/<int:pk>/', RepeatDataView, name='repeatdata'),
    path('confirm/top/<int:pk>/', ConfirmTopView, name='confirmtop'),
    path('validate/top/<int:pk>/', ValidateTopView, name='validatetop'),
    path('beneficiary/', BeneficiaryView, name='beneficiary'),
    path('add/beneficiary/', AddBeneficiaryView, name='addbeneficiary'),
    path('confirm/beneficiary/<int:pk>/', ConfirmBeneficiaryView, name='confirmbeneficiary'),
    path('validate/beneficiary/<int:pk>/', ValidateBeneficiaryView, name='validatebeneficiary'),
    path('remove/beneficiary/', RemoveBeneficiaryView, name='removebeneficiary'),
    path('beneficiary/transfer/<int:pk>/', BeneficiaryTransferView, name='beneficiarytransfer'),
    path('service/', ServiceView, name='service'),
    path('card/', CardView, name='card'),
    path('validate/card/', ValidateCardView, name='validatecard'),
    path('modify/limit/', ModifyLimitView, name='modify'),
    path('validate/modify/', ValidateModifyView, name='validatemodify'),
    path('statement/', StatementView, name='statement'),
    path('download/statement/<start>/<stop>/', DownloadStatementView),
    path('locate/', LocateView, name='locate'),
    path('contact/', ContactView, name='contact'),
    path('profile/', ProfileView, name='profile'),
    path('setting/', SettingView, name='setting'),
    path('change/user_id/', ChangeUserIDView, name='changeuserid'),
    path('change/pin/', ChangePinView, name='changepin'),
    path('confirm/pin/', ConfirmPinView, name='confirmpin'),
    path('support/', SupportView, name='support'),
    path('faq/', FAQView, name='faq'),
    path('loan/', LoanView, name='loan'),
    path('laon/detail/<int:pk>/', LoanDetailView, name='loandetail'),
    path('calculate/interest/', CalculatorView, name='calculate'),
    path('pay/loan/<int:pk>/', PayLoanView, name='payloan'),
    path('messages/', MessageView, name='message'),
    path('message/detail/<int:pk>/', DetailMessageView, name='detailmessage'),
    path('fund/wallet/', FundWalletView, name='fund_wallet'),
	path('payment/<str:ref>/', VerifyPaymentView, name='verify_payment'),
]
