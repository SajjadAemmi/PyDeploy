from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, SignInForm


def index(request):
    return render(request, 'shop/index.html')

def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = SignUpForm()
    return render(request, 'shop/signup.html', {'form': form})

def signin_view(request):
    if request.method == "POST":
        form = SignInForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile')
    else:
        form = SignInForm()
    return render(request, 'shop/signin.html', {'form': form})

def signout_view(request):
    logout(request)
    return redirect('signin')

@login_required
def profile_view(request):
    return render(request, 'shop/profile.html', {'user': request.user})
