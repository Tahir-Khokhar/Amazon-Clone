from django.urls import path
from .views import HealthCheckView, APIRootView, SiteConfigurationView, ShippingRulesView, ReturnPolicyView, PaymentMethodsView, SupportInfoView, NewsletterSubscribeView, SubscriptionPageView, SubscriptionCreateView, SubscriptionConfirmView

app_name = 'core'

urlpatterns = [
    path('health/', HealthCheckView.as_view(), name='health'),
    path('api-root/', APIRootView.as_view(), name='api-root'),
    path('settings/', SiteConfigurationView.as_view(), name='site-config'),
    path('shipping/rules/', ShippingRulesView.as_view(), name='shipping-rules'),
    path('returns/policy/', ReturnPolicyView.as_view(), name='return-policy'),
    path('payments/methods/', PaymentMethodsView.as_view(), name='payment-methods'),
    path('support/info/', SupportInfoView.as_view(), name='support-info'),
    path('newsletter/subscribe/', NewsletterSubscribeView.as_view(), name='newsletter-subscribe'),
    path('subscribe/premium/', SubscriptionPageView.as_view(), name='subscription-page'),
    path('subscribe/create/', SubscriptionCreateView.as_view(), name='subscription-create'),
    path('subscribe/confirm/', SubscriptionConfirmView.as_view(), name='subscription-confirm'),
]
