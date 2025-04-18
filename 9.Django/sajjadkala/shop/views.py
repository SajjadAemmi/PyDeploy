from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.http import JsonResponse
from .forms import SignUpForm, SignInForm
from .models import Product, CartItem


def index(request):
    products = Product.objects.order_by('-id')[:4]
    return render(request, 'index.html', {
        'products': products
    })


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


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Get or create a session key
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key

    # Check if item is already in cart
    cart_item, created = CartItem.objects.get_or_create(
        product=product,
        session_key=session_key,
        defaults={'quantity': 1}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')


def cart(request):
    session_key = request.session.session_key
    cart_items = CartItem.objects.filter(session_key=session_key)

    total = sum(item.total_price() for item in cart_items)

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total,
    })


def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    return redirect('cart')


def api_all_products(request):
    products = Product.objects.all().values(
        'id', 'name', 'price', 'brand', 'category', 'description'
    )
    return JsonResponse(list(products), safe=False, json_dumps_params={'ensure_ascii': False})
