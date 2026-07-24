from django.urls import path
from .views import (
    MyReferralCodeView,
    ReferralListView,
    ApplyReferralView,
)

app_name = 'referrals'

urlpatterns = [
    path('my-code/', MyReferralCodeView.as_view(), name='my-code'),
    path('list/', ReferralListView.as_view(), name='referral-list'),
    path('apply/', ApplyReferralView.as_view(), name='apply-referral'),
]
