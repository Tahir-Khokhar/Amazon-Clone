from django.shortcuts import render

def home(request):
    return render(request, 'frontend/home.html')

def products(request):
    return render(request, 'frontend/products.html')

def cart(request):
    return render(request, 'frontend/cart.html')

def wishlist(request):
    return render(request, 'frontend/wishlist.html')

def login(request):
    return render(request, 'frontend/login.html')

def register(request):
    return render(request, 'frontend/register.html')

def profile(request):
    return render(request, 'frontend/profile.html')
