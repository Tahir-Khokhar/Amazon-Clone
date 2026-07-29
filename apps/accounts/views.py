from django.contrib.auth import get_user_model, login as auth_login
from django.conf import settings
from rest_framework import generics, permissions, serializers, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
import pyotp

from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    ProfileSerializer,
    ProfilePictureSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
    ChangePasswordSerializer,
    UserSerializer,
)
from .models import Profile

User = get_user_model()


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        user_data = UserSerializer(user).data
        auth_login(request, user)
        return Response({
            "message": "User registered successfully.",
            "user": user_data,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        if user.two_factor_enabled:
            code = request.data.get('two_factor_code')
            if not code:
                return Response({
                    'detail': '2FA code required.',
                    'requires_2fa': True,
                }, status=status.HTTP_200_OK)
            totp = pyotp.TOTP(user.two_factor_secret)
            if not totp.verify(code):
                return Response({'error': 'Invalid 2FA code.'}, status=status.HTTP_400_BAD_REQUEST)
        
        tokens = serializer.get_tokens(user)
        user_data = UserSerializer(user).data
        auth_login(request, user)
        return Response({
            'user': user_data,
            'access': tokens['access'],
            'refresh': tokens['refresh'],
        }, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.Serializer

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data.get("refresh")
            if refresh_token is None:
                return Response(
                    {"detail": "Refresh token is required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {"message": "Logged out successfully."},
                status=status.HTTP_205_RESET_CONTENT,
            )
        except TokenError:
            return Response(
                {"detail": "Invalid or expired refresh token."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class RefreshTokenView(generics.GenericAPIView):
    serializer_class = serializers.Serializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get("refresh")
        if refresh_token is None:
            return Response(
                {"detail": "Refresh token is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            token = RefreshToken(refresh_token)
            return Response(
                {"access": str(token.access_token)},
                status=status.HTTP_200_OK,
            )
        except TokenError:
            return Response(
                {"detail": "Invalid or expired refresh token."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ForgotPasswordView(generics.GenericAPIView):
    serializer_class = ForgotPasswordSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        try:
            user = User.objects.get(email=email)
            from django.contrib.auth.tokens import default_token_generator
            from django.utils.http import urlsafe_base64_encode
            from django.utils.encoding import force_bytes
            from django.core.mail import send_mail
            from django.conf import settings as django_settings

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_url = f"{getattr(django_settings, 'FRONTEND_URL', 'http://localhost:3000')}/reset-password/{uid}/{token}/"
            send_mail(
                "Password Reset Request",
                f"Click the link to reset your password:\n{reset_url}",
                django_settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
        except User.DoesNotExist:
            pass
        return Response(
            {"message": "If an account with that email exists, a password reset link has been sent."},
            status=status.HTTP_200_OK,
        )


class ResetPasswordView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data['token']

        from django.contrib.auth.tokens import default_token_generator
        from django.utils.http import urlsafe_base64_decode
        from django.utils.encoding import force_str

        uid = request.data.get("uid")
        if not uid:
            return Response(
                {"detail": "uid is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=user_id)
        except (User.DoesNotExist, ValueError, TypeError):
            return Response(
                {"detail": "Invalid reset link."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not default_token_generator.check_token(user, token):
            return Response(
                {"detail": "Invalid or expired token."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(serializer.validated_data['password'])
        user.save()
        return Response(
            {"message": "Password reset successfully."},
            status=status.HTTP_200_OK,
        )


class ChangePasswordView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response(
            {"message": "Password changed successfully."},
            status=status.HTTP_200_OK,
        )


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        profile = self.request.user.profile
        if profile is None:
            profile = Profile.objects.create(user=self.request.user)
        return profile

    def get(self, request, *args, **kwargs):
        if request.query_params.get('fields') == 'user':
            user_serializer = UserSerializer(request.user)
            return Response(user_serializer.data)
        return super().get(request, *args, **kwargs)


class ProfilePictureView(generics.UpdateAPIView):
    serializer_class = ProfilePictureSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post', 'put', 'patch']

    def get_object(self):
        return self.request.user.profile

    def post(self, request, *args, **kwargs):
        profile = self.get_object()
        old_image = profile.profile_picture
        serializer = self.get_serializer(profile, data={'profile_picture': request.data.get('profile_picture')})
        serializer.is_valid(raise_exception=True)
        if old_image and old_image != serializer.validated_data.get('profile_picture', old_image):
            old_image.delete(save=False)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        profile = self.get_object()
        old_image = profile.profile_picture
        serializer = self.get_serializer(profile, data={'profile_picture': request.data.get('profile_picture')})
        serializer.is_valid(raise_exception=True)
        if old_image and old_image != serializer.validated_data.get('profile_picture', old_image):
            old_image.delete(save=False)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfilePictureDeleteView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.Serializer

    def delete(self, request, *args, **kwargs):
        profile = request.user.profile
        if profile.profile_picture:
            profile.profile_picture.delete(save=True)
            profile.save()
        return Response({"message": "Profile picture removed successfully."}, status=status.HTTP_200_OK)


class MeView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class SocialAuthView(generics.GenericAPIView):
    serializer_class = __import__('apps.accounts.serializers', fromlist=['SocialAuthSerializer']).SocialAuthSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        from apps.accounts.serializers import SocialAuthSerializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        user, created = User.objects.get_or_create(
            social_id=data['email'],
            defaults={
                'username': data['username'],
                'email': data['email'],
                'first_name': data.get('first_name', ''),
                'last_name': data.get('last_name', ''),
                'social_provider': data['provider'],
                'is_verified': True,
            }
        )

        if not created:
            if not user.social_provider:
                user.social_provider = data['provider']
                user.save()

        tokens = LoginSerializer().get_tokens(user)
        user_data = UserSerializer(user).data
        return Response({
            'user': user_data,
            'access': tokens['access'],
            'refresh': tokens['refresh'],
        }, status=status.HTTP_200_OK)


class TwoFactorSetupView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = __import__('apps.accounts.serializers', fromlist=['TwoFactorSetupSerializer']).TwoFactorSetupSerializer

    def post(self, request, *args, **kwargs):
        from apps.accounts.serializers import TwoFactorSetupSerializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user

        if not user.two_factor_secret:
            secret = pyotp.random_base32()
            user.two_factor_secret = secret
            user.save()

        totp = pyotp.TOTP(user.two_factor_secret)
        provisioning_uri = totp.provisioning_uri(name=user.email, issuer_name=getattr(settings, 'SITE_NAME', 'Amazon Clone'))
        return Response({
            'secret': user.two_factor_secret,
            'provisioning_uri': provisioning_uri,
        }, status=status.HTTP_200_OK)


class TwoFactorVerifyView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = __import__('apps.accounts.serializers', fromlist=['TwoFactorVerifySerializer']).TwoFactorVerifySerializer

    def post(self, request, *args, **kwargs):
        from apps.accounts.serializers import TwoFactorVerifySerializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        code = serializer.validated_data['code']

        totp = pyotp.TOTP(user.two_factor_secret)
        if totp.verify(code):
            user.two_factor_enabled = True
            user.save()
            return Response({'message': '2FA enabled successfully.'}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid code.'}, status=status.HTTP_400_BAD_REQUEST)


class TwoFactorDisableView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = __import__('apps.accounts.serializers', fromlist=['TwoFactorDisableSerializer']).TwoFactorDisableSerializer

    def post(self, request, *args, **kwargs):
        from apps.accounts.serializers import TwoFactorDisableSerializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        user.two_factor_enabled = False
        user.two_factor_secret = ''
        user.save()
        return Response({'message': '2FA disabled successfully.'}, status=status.HTTP_200_OK)
