from django.urls import path
from .views import (
    ProductQuestionListView,
    ProductQuestionDetailView,
    ProductQuestionCreateView,
    ProductAnswerCreateView,
    MarkAnswerHelpfulView,
)

app_name = 'product_qa'

urlpatterns = [
    path('products/<slug:product_slug>/questions/', ProductQuestionListView.as_view(), name='question-list'),
    path('products/<slug:product_slug>/questions/create/', ProductQuestionCreateView.as_view(), name='question-create'),
    path('questions/<int:pk>/', ProductQuestionDetailView.as_view(), name='question-detail'),
    path('questions/<int:pk>/answers/create/', ProductAnswerCreateView.as_view(), name='answer-create'),
    path('answers/<int:pk>/helpful/', MarkAnswerHelpfulView.as_view(), name='answer-helpful'),
]
