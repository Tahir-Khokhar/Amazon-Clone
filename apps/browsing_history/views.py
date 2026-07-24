from rest_framework import generics, permissions, status

from .models import BrowsingHistory
from .serializers import BrowsingHistorySerializer
from rest_framework.response import Response


class BrowsingHistoryListView(generics.ListAPIView):
    serializer_class = BrowsingHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return BrowsingHistory.objects.filter(user=self.request.user)[:50]


class BrowsingHistoryClearView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        BrowsingHistory.objects.filter(user=request.user).delete()
        return Response({"message": "Browsing history cleared."}, status=status.HTTP_204_NO_CONTENT)
