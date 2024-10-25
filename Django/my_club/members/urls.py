from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('members/', views.members, name='members'),
    path('members/details/<int:id>', views.details, name='details'),
    path('a/', views.b, name='c'),
    path('a2/', views.b2, name='c2'),
    path('testing/', views.testing, name='testing'),
]
