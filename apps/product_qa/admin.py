from django.contrib import admin
from .models import ProductQuestion, ProductAnswer

@admin.register(ProductQuestion)
class ProductQuestionAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'question', 'is_answered', 'created_at']
    list_filter = ['is_answered', 'created_at']
    search_fields = ['question', 'user__username', 'product__name']

@admin.register(ProductAnswer)
class ProductAnswerAdmin(admin.ModelAdmin):
    list_display = ['question', 'user', 'answer', 'is_official', 'created_at']
    list_filter = ['is_official', 'created_at']
    search_fields = ['answer', 'user__username']
