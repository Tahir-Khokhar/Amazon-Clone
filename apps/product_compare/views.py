from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .models import CompareList, CompareItem
from .serializers import CompareListSerializer, CompareItemSerializer


class CompareListView(generics.RetrieveAPIView):
    serializer_class = CompareListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        compare_list, _ = CompareList.objects.get_or_create(user=self.request.user)
        return compare_list


class AddToCompareView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CompareItemSerializer

    def post(self, request, *args, **kwargs):
        product_id = kwargs.get('product_id')
        product = get_object_or_404(__import__('apps.products.models', fromlist=['Product']).Product, pk=product_id, is_active=True)
        compare_list, _ = CompareList.objects.get_or_create(user=request.user)
        item, created = CompareItem.objects.get_or_create(compare_list=compare_list, product=product)
        if created:
            return Response({"message": "Added to compare list."}, status=status.HTTP_201_CREATED)
        return Response({"message": "Already in compare list."}, status=status.HTTP_200_OK)


class RemoveFromCompareView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        product_id = kwargs.get('product_id')
        compare_list = get_object_or_404(CompareList, user=request.user)
        item = get_object_or_404(CompareItem, compare_list=compare_list, product_id=product_id)
        item.delete()
        return Response({"message": "Removed from compare list."}, status=status.HTTP_204_NO_CONTENT)


class ClearCompareView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        compare_list = get_object_or_404(CompareList, user=request.user)
        compare_list.items.all().delete()
        return Response({"message": "Compare list cleared."}, status=status.HTTP_204_NO_CONTENT)
