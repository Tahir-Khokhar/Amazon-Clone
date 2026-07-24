from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .models import ProductQuestion, ProductAnswer
from .serializers import ProductQuestionSerializer, ProductQuestionCreateSerializer, ProductAnswerSerializer, ProductAnswerCreateSerializer


class ProductQuestionListView(generics.ListAPIView):
    serializer_class = ProductQuestionSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        product_slug = self.kwargs.get('product_slug')
        return ProductQuestion.objects.filter(product__slug=product_slug)


class ProductQuestionDetailView(generics.RetrieveAPIView):
    queryset = ProductQuestion.objects.all()
    serializer_class = ProductQuestionSerializer
    permission_classes = [permissions.AllowAny]


class ProductQuestionCreateView(generics.CreateAPIView):
    serializer_class = ProductQuestionCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        product_slug = self.kwargs.get('product_slug')
        product = get_object_or_404(__import__('apps.products.models', fromlist=['Product']).Product, slug=product_slug)
        serializer.save(product=product, user=self.request.user)


class ProductAnswerCreateView(generics.CreateAPIView):
    serializer_class = ProductAnswerCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MarkAnswerHelpfulView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        answer = get_object_or_404(ProductAnswer, pk=kwargs.get('pk'))
        answer.helpful_count += 1
        answer.save(update_fields=['helpful_count'])
        return Response({"message": "Marked as helpful.", "helpful_count": answer.helpful_count}, status=status.HTTP_200_OK)
