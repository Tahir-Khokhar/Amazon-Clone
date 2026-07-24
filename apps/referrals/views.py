from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .models import ReferralCode, Referral
from .serializers import ReferralCodeSerializer, ReferralSerializer


class MyReferralCodeView(generics.RetrieveAPIView):
    serializer_class = ReferralCodeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        code, _ = ReferralCode.objects.get_or_create(user=self.request.user)
        return code


class ReferralListView(generics.ListAPIView):
    serializer_class = ReferralSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Referral.objects.filter(referrer=self.request.user)


class ApplyReferralView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReferralSerializer

    def post(self, request, *args, **kwargs):
        code = request.data.get('code')
        if not code:
            return Response({"error": "Referral code is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            referral_code = ReferralCode.objects.get(code=code, is_active=True)
        except ReferralCode.DoesNotExist:
            return Response({"error": "Invalid referral code."}, status=status.HTTP_404_NOT_FOUND)
        
        if referral_code.user == request.user:
            return Response({"error": "You cannot use your own referral code."}, status=status.HTTP_400_BAD_REQUEST)
        
        existing = Referral.objects.filter(referred_user=request.user).exists()
        if existing:
            return Response({"error": "You have already used a referral code."}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"message": "Referral code is valid. Use it during checkout."}, status=status.HTTP_200_OK)
