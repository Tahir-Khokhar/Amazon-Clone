from django.urls import path
from .views import (
    ReviewListView,
    ReviewDetailView,
    ReviewCreateView,
    ReviewUpdateView,
    ReviewDeleteView,
    LikeReviewView,
    ReportReviewView,
)

app_name = 'reviews'

urlpatterns = [
    path('', ReviewListView.as_view(), name='review-list'),
    path('<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
    path('create/', ReviewCreateView.as_view(), name='review-create'),
    path('<int:pk>/update/', ReviewUpdateView.as_view(), name='review-update'),
    path('<int:pk>/delete/', ReviewDeleteView.as_view(), name='review-delete'),
    path('<int:pk>/like/', LikeReviewView.as_view(), name='review-like'),
    path('<int:pk>/report/', ReportReviewView.as_view(), name='review-report'),
]
