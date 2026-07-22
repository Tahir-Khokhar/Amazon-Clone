from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .models import Review, ReviewLike
from .serializers import ReviewSerializer, ReviewLikeSerializer, ReviewReportSerializer


class ReviewListView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Review.objects.filter(is_approved=True)
        product_id = self.request.query_params.get("product_id")
        if product_id:
            queryset = queryset.filter(product_id=product_id)
        return queryset


class ReviewDetailView(generics.RetrieveAPIView):
    queryset = Review.objects.filter(is_approved=True)
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]


class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReviewUpdateView(generics.UpdateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)


class ReviewDeleteView(generics.DestroyAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)


class LikeReviewView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        review = get_object_or_404(Review, pk=kwargs.get("pk"))
        like, created = ReviewLike.objects.get_or_create(review=review, user=request.user)
        if created:
            review.helpful_count = ReviewLike.objects.filter(review=review).count()
            review.save()
            return Response({"message": "Review liked."}, status=status.HTTP_201_CREATED)
        like.delete()
        review.helpful_count = ReviewLike.objects.filter(review=review).count()
        review.save()
        return Response({"message": "Like removed."}, status=status.HTTP_200_OK)


class ReportReviewView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReviewReportSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        review = get_object_or_404(Review, pk=kwargs.get("pk"))
        review.is_approved = False
        review.save()
        return Response(
            {"message": "Review reported. It will be reviewed by moderators."},
            status=status.HTTP_200_OK,
        )
