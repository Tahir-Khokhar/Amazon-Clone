from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Sum
from django.contrib import messages

from apps.products.models import Product
from apps.categories.models import Category
from apps.cart.models import Cart
from apps.orders.models import Order, OrderItem
from apps.returns.models import ReturnRequest
from apps.support.models import SupportTicket, TicketMessage
from apps.reviews.models import Review


def _get_cart_count(request):
    """Get cart item count for current user/session."""
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user, status="active").first()
    else:
        session_key = request.session.session_key
        if not session_key:
            return 0
        cart = Cart.objects.filter(session_key=session_key, status="active").first()
    if not cart:
        return 0
    result = cart.items.aggregate(total=Sum('quantity'))
    return result['total'] or 0


def home(request):
    featured_products = Product.objects.filter(
        is_active=True,
        is_featured=True
    ).select_related('brand', 'category', 'seller').prefetch_related('images')[:8]
    
    categories = Category.objects.filter(
        is_active=True, parent__isnull=True
    ).prefetch_related('children')[:8]

    deal_products = Product.objects.filter(
        is_active=True,
        discount_price__isnull=False
    ).select_related('brand', 'category').prefetch_related('images')[:4]

    new_arrivals = Product.objects.filter(
        is_active=True
    ).select_related('brand', 'category').prefetch_related('images').order_by('-created_at')[:4]

    search_query = request.GET.get('q', '')
    cart_count = _get_cart_count(request)

    context = {
        'featured_products': featured_products,
        'categories': categories,
        'deal_products': deal_products,
        'new_arrivals': new_arrivals,
        'search_query': search_query,
        'cart_count': cart_count,
    }
    return render(request, 'frontend/home.html', context)

def products(request):
    products_qs = Product.objects.filter(
        is_active=True
    ).select_related('brand', 'category', 'seller').prefetch_related('images')

    category_slug = request.GET.get('category')
    if category_slug:
        products_qs = products_qs.filter(category__slug=category_slug)

    search_query = request.GET.get('q')
    if search_query:
        products_qs = products_qs.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    products_qs = products_qs.order_by('-created_at')[:48]

    context = {
        'products': products_qs,
        'search_query': search_query or '',
    }
    return render(request, 'frontend/products.html', context)

def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects.select_related('brand', 'category', 'seller').prefetch_related('images'),
        slug=slug,
        is_active=True,
    )
    related_products = Product.objects.filter(
        category=product.category,
        is_active=True,
    ).exclude(id=product.id).select_related('brand', 'category', 'seller').prefetch_related('images')[:8]

    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'frontend/product_detail.html', context)

def categories(request):
    categories_qs = Category.objects.filter(is_active=True).prefetch_related('children')

    categories_with_products = []
    for category in categories_qs:
        product_count = Product.objects.filter(category=category, is_active=True).count()
        categories_with_products.append({
            'category': category,
            'product_count': product_count,
        })

    context = {
        'categories_with_products': categories_with_products,
    }
    return render(request, 'frontend/categories.html', context)

def deals(request):
    deals_qs = Product.objects.filter(
        is_active=True,
        discount_price__isnull=False
    ).select_related('brand', 'category', 'seller').prefetch_related('images').order_by('-discount_price')[:48]

    context = {
        'products': deals_qs,
        'search_query': '',
    }
    return render(request, 'frontend/deals.html', context)

def cart(request):
    from apps.cart.models import Cart
    from apps.core.models import SiteConfiguration
    from decimal import Decimal

    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user, status="active").prefetch_related('items__product', 'items__variant').first()
        addresses = request.user.addresses.all()
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart = Cart.objects.filter(session_key=session_key, status="active").prefetch_related('items__product', 'items__variant').first()
        addresses = []

    subtotal = Decimal('0.00')
    if cart and cart.items.exists():
        for item in cart.items.all():
            subtotal += (item.product.price or Decimal('0.00')) * item.quantity
        messages.success(request, f'You have {cart.items.count()} item(s) in your cart.')

    config = SiteConfiguration.get_active()
    shipping = Decimal('0.00')
    free_shipping_threshold = config.free_shipping_threshold if config else Decimal('50.00')
    if cart and cart.items.exists() and subtotal < free_shipping_threshold:
        shipping = config.standard_shipping_cost if config else Decimal('5.00')

    tax = (subtotal * Decimal('0.05')).quantize(Decimal('0.01'))
    total = subtotal + shipping + tax

    context = {
        'cart': cart,
        'subtotal': subtotal,
        'shipping': shipping,
        'tax': tax,
        'total': total,
        'addresses': addresses,
        'user': request.user,
        'free_shipping_threshold': free_shipping_threshold,
        'free_shipping_remaining': max(free_shipping_threshold - subtotal, 0) if subtotal < free_shipping_threshold else 0,
    }
    return render(request, 'frontend/cart.html', context)

def wishlist(request):
    return render(request, 'frontend/wishlist.html')

def login(request):
    return render(request, 'frontend/login.html')

def register(request):
    return render(request, 'frontend/register.html')

def profile(request):
    if not request.user.is_authenticated:
        return render(request, 'frontend/login.html')
    orders = Order.objects.filter(user=request.user).order_by('-ordered_at')[:5]
    pending_count = orders.filter(order_status='pending').count()
    processing_count = orders.filter(order_status__in=['confirmed', 'packed']).count()
    shipped_count = orders.filter(order_status__in=['shipped', 'out_for_delivery']).count()
    delivered_count = orders.filter(order_status='delivered').count()
    cancelled_count = orders.filter(order_status='cancelled').count()
    returned_count = orders.filter(order_status='returned').count()
    return_requests = ReturnRequest.objects.filter(user=request.user).order_by('-created_at')[:5]
    support_tickets = SupportTicket.objects.filter(user=request.user).order_by('-created_at')[:5]
    reviews = Review.objects.filter(user=request.user).order_by('-created_at')[:5]
    context = {
        'orders': orders,
        'pending_count': pending_count,
        'processing_count': processing_count,
        'shipped_count': shipped_count,
        'delivered_count': delivered_count,
        'cancelled_count': cancelled_count,
        'returned_count': returned_count,
        'return_requests': return_requests,
        'support_tickets': support_tickets,
        'reviews': reviews,
    }
    return render(request, 'frontend/profile.html', context)


def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, 'frontend/order_detail.html', {'order': order})


def order_history(request):
    if not request.user.is_authenticated:
        return render(request, 'frontend/login.html')
    orders = Order.objects.filter(user=request.user).order_by('-ordered_at')
    status_filter = request.GET.get('status')
    if status_filter:
        orders = orders.filter(order_status=status_filter)
    context = {
        'orders': orders,
        'status_filter': status_filter or '',
    }
    return render(request, 'frontend/orders.html', context)

def support_home(request):
    from apps.support.models import SupportCategory, FAQ
    categories = SupportCategory.objects.filter(is_active=True)
    faqs = FAQ.objects.filter(is_active=True)[:10]
    return render(request, 'frontend/support.html', {'categories': categories, 'faqs': faqs})

def faqs(request):
    return render(request, 'frontend/faqs.html')

def contact_us(request):
    return render(request, 'frontend/contact_us.html')

def return_request(request):
    order_id = request.GET.get('order')
    order = None
    if order_id:
        order = get_object_or_404(Order, pk=order_id, user=request.user)
    return render(request, 'frontend/return_request.html', {'order': order})


def shipping_policy(request):
    return render(request, 'frontend/shipping_policy.html')


def return_policy(request):
    return render(request, 'frontend/return_policy.html')


def privacy_policy(request):
    return render(request, 'frontend/privacy_policy.html')


def terms(request):
    return render(request, 'frontend/terms.html')
