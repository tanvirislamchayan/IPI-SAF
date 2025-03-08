from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.auth_login, name='auth_login'),
    path('create/', views.auth_create, name='auth_create'),
    path('institute/', views.institute, name='manage_college'),
]