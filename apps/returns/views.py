from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from rest_framework import generics, permissions, serializers, status
from rest_framework.response import Response

from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderCreateSerializer


class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Order.objects.none()

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Order.objects.none()
        return Order.objects.filter(user=self.request.user)


class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Order.objects.none()

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Order.objects.none()
        return Order.objects.filter(user=self.request.user)


class OrderCreateView(generics.CreateAPIView):
    serializer_class = OrderCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        from decimal import Decimal
        from apps.cart.models import Cart, CartItem
        from apps.coupons.models import Coupon
        from apps.core.models import SiteConfiguration
        
        user = self.request.user
        validated_data = serializer.validated_data
        
        cart = Cart.objects.filter(user=user, status='active').first()
        if not cart or not cart.items.filter(is_saved_for_later=False).exists():
            raise serializers.ValidationError('Cart is empty.')
        
        cart_items = cart.items.filter(is_saved_for_later=False)
        
        subtotal = sum(item.product.price * item.quantity for item in cart_items)
        
        tax_rate = Decimal(str(validated_data.get('tax_rate', 0)))
        tax_amount = (subtotal * tax_rate) / Decimal('100')
        
        is_gift = validated_data.get('is_gift', False)
        gift_wrap = validated_data.get('gift_wrap', False)
        gift_wrap_fee = Decimal('5.00') if gift_wrap else Decimal('0')
        
        config = SiteConfiguration.get_active()
        shipping_cost = Decimal('0')
        if config:
            if subtotal >= config.free_shipping_threshold:
                shipping_cost = Decimal('0')
            else:
                shipping_address_id = validated_data.get('shipping_address_id')
                try:
                    from apps.addresses.models import Address
                    address = Address.objects.get(pk=shipping_address_id, user=user)
                    shipping_cost = config.standard_shipping_cost if address.city in ['Karachi', 'Lahore', 'Islamabad'] else Decimal('100.00')
                except Exception:
                    shipping_cost = config.standard_shipping_cost
        else:
            shipping_address_id = validated_data.get('shipping_address_id')
            try:
                from apps.addresses.models import Address
                address = Address.objects.get(pk=shipping_address_id, user=user)
                shipping_cost = Decimal('50.00') if address.city in ['Karachi', 'Lahore', 'Islamabad'] else Decimal('100.00')
            except Exception:
                shipping_cost = Decimal('100.00')
        
        discount_amount = Decimal('0')
        coupon = None
        coupon_code = validated_data.get('coupon_code')
        if coupon_code:
            try:
                coupon = Coupon.objects.get(code=coupon_code, is_active=True)
                if coupon.is_valid():
                    if coupon.discount_type == 'flat':
                        discount_amount = min(coupon.discount_value, subtotal)
                    elif coupon.discount_type == 'percentage':
                        discount_amount = (subtotal * coupon.discount_value) / Decimal('100')
                        if coupon.max_discount_amount:
                            discount_amount = min(discount_amount, coupon.max_discount_amount)
            except Coupon.DoesNotExist:
                pass
        
        grand_total = subtotal + shipping_cost + tax_amount + gift_wrap_fee - discount_amount

        from datetime import datetime
        import uuid
        order_number = f"ORD-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"

        shipping_address = None
        if shipping_address_id:
            from apps.shipping.models import ShippingAddress
            try:
                shipping_address = ShippingAddress.objects.get(pk=shipping_address_id, user=user)
            except ShippingAddress.DoesNotExist:
                from apps.addresses.models import Address
                try:
                    addr = Address.objects.get(pk=shipping_address_id, user=user)
                    shipping_address, _ = ShippingAddress.objects.get_or_create(
                        user=user,
                        street_address=addr.street_address,
                        city=addr.city,
                        postal_code=addr.postal_code,
                        defaults={
                            'full_name': addr.full_name,
                            'phone_number': addr.phone_number,
                            'state': addr.state,
                            'country': addr.country,
                            'is_default': addr.is_default,
                        },
                    )
                except Address.DoesNotExist:
                    pass
        
        order = Order.objects.create(
            user=user,
            order_number=order_number,
            subtotal=subtotal,
            shipping_cost=shipping_cost,
            tax_rate=tax_rate,
            tax_amount=tax_amount,
            discount_amount=discount_amount,
            grand_total=grand_total,
            coupon=coupon,
            shipping_address_id=shipping_address_id,
            billing_address_id=validated_data.get('billing_address_id'),
            payment_method=validated_data.get('payment_method'),
            notes=validated_data.get('notes', ''),
            is_gift=is_gift,
            gift_message=validated_data.get('gift_message', ''),
            gift_wrap=gift_wrap,
            gift_wrap_fee=gift_wrap_fee,
        )
        
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                variant=cart_item.variant,
                product_name=cart_item.product.name,
                product_sku=cart_item.product.sku,
                quantity=cart_item.quantity,
                unit_price=cart_item.product.price,
                total_price=cart_item.product.price * cart_item.quantity,
                is_gift=is_gift,
            )
        
        for item in cart_items:
            item.product.reduce_stock(item.quantity)
        
        cart.items.filter(is_saved_for_later=False).delete()


class OrderCancelView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer
    queryset = Order.objects.none()

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Order.objects.none()
        return Order.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        order = self.get_object()
        if order.order_status not in ["pending", "confirmed"]:
            return Response(
                {"detail": "Order cannot be cancelled at this stage."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        order.order_status = "cancelled"
        order.save()
        return Response({"message": "Order cancelled successfully."}, status=status.HTTP_200_OK)


class AdminOrderListView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAdminUser]


class SellerOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Order.objects.none()

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Order.objects.none()
        return Order.objects.filter(items__product__seller=self.request.user).distinct()


class DeliveryOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Order.objects.none()

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Order.objects.none()
        user = self.request.user
        if user.role == "delivery":
            return Order.objects.filter(order_status__in=["shipped", "out_for_delivery"])
        return Order.objects.none()


class OrderInvoiceView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer

    def get(self, request, *args, **kwargs):
        order = get_object_or_404(Order, pk=kwargs.get('pk'), user=request.user)
        template = get_template('orders/invoice.html')
        html = template.render({'order': order})
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="invoice_{order.order_number}.pdf"'
        try:
            from weasyprint import HTML
            HTML(string=html).write_pdf(response)
        except Exception:
            response = HttpResponse(html, content_type='text/html')
            response['Content-Disposition'] = f'attachment; filename="invoice_{order.order_number}.html"'
        return response
