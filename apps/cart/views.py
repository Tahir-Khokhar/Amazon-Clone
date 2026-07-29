from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer


def _merge_carts(user, session_key):
    if not session_key:
        return
    session_cart = Cart.objects.filter(session_key=session_key, status="active").first()
    if not session_cart:
        return
    user_cart, _ = Cart.objects.get_or_create(user=user, status="active")
    for item in session_cart.items.all():
        existing = user_cart.items.filter(product=item.product, variant=item.variant).first()
        if existing:
            existing.quantity += item.quantity
            existing.save()
        else:
            item.cart = user_cart
            item.save()
    session_cart.status = 'merged'
    session_cart.save()


def _get_cart(request):
    if request.user.is_authenticated:
        if request.session.session_key:
            _merge_carts(request.user, request.session.session_key)
        cart, _ = Cart.objects.get_or_create(user=request.user, status="active")
        return cart
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key
    cart, _ = Cart.objects.get_or_create(session_key=session_key, status="active")
    return cart


class CartListView(generics.ListAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Cart.objects.none()

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Cart.objects.none()
        cart = _get_cart(self.request)
        return Cart.objects.filter(pk=cart.pk)


class CartDetailView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Cart.objects.none()

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Cart.objects.none()
        cart = _get_cart(self.request)
        return Cart.objects.filter(pk=cart.pk)


class CartItemCreateView(generics.CreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        cart = _get_cart(self.request)
        product = serializer.validated_data.get('product')
        variant = serializer.validated_data.get('variant')
        quantity = serializer.validated_data.get('quantity', 1)
        existing = CartItem.objects.filter(cart=cart, product=product, variant=variant).first()
        if existing:
            existing.quantity += quantity
            existing.save()
        else:
            serializer.save(cart=cart)


class CartItemUpdateView(generics.UpdateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.AllowAny]
    queryset = CartItem.objects.none()

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return CartItem.objects.none()
        cart = _get_cart(self.request)
        return CartItem.objects.filter(cart=cart)


class CartItemDeleteView(generics.DestroyAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.AllowAny]
    queryset = CartItem.objects.none()

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return CartItem.objects.none()
        cart = _get_cart(self.request)
        return CartItem.objects.filter(cart=cart)
