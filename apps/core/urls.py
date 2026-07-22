from django.urls import path
from .views import HealthCheckView, APIRootView

app_name = 'core'

urlpatterns = [
    path('health/', HealthCheckView.as_view(), name='health'),
    path('api-root/', APIRootView.as_view(), name='api-root'),
]
