from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import SignUpForm, SignInForm
from .models import Product


def index(request):
    return render(request, 'index.html')


def product(request, product_id: int):
    product = Product.objects.get(id=product_id)
    return render(request, 'product.html', {
        'product': product
    })


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')

    elif request.method == 'GET':
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def signin(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile')
        
    elif request.method == 'GET':
        form = SignInForm()
    return render(request, 'signin.html', {'form': form})


def signout(request):
    logout(request)
    return redirect('index')

def profile(request):
    return render(request, 'profile.html', {'user': request.user})

def products(request):
    products = Product.objects.all()
    return render(request, 'products.html', {
        'products': products
    })

def cart(request):
    pass

def add_to_cart(request, product_id: int):
    pass
