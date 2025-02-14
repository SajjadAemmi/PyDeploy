from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Customer

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Customer
        fields = ['username', 'email', 'phone', 'address', 'password1', 'password2']

class SignInForm(AuthenticationForm):
    pass
