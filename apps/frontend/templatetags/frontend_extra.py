from django import template
from django.contrib.auth import get_user_model

register = template.Library()

User = get_user_model()


@register.filter
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except (TypeError, ValueError):
        return ''


@register.filter
def mul(value, arg):
    try:
        return int(value) * int(arg)
    except (TypeError, ValueError):
        return 0


@register.filter
def currency(value):
    try:
        return f"${float(value):.2f}"
    except (TypeError, ValueError):
        return ''


@register.simple_tag(takes_context=True)
def cart_item_count(context):
    request = context.get('request')
    if not request:
        return 0
    from apps.cart.models import Cart
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user, status="active").first()
    else:
        session_key = request.session.session_key
        if not session_key:
            return 0
        cart = Cart.objects.filter(session_key=session_key, status="active").first()
    if not cart:
        return 0
    return sum(item.quantity for item in cart.items.all())


@register.simple_tag
def user_count():
    return User.objects.filter(is_active=True).count()
