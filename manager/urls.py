from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.auth_login, name='auth_login'),
    path('create/', views.auth_create, name='auth_create'),
    path('institute/', views.institute, name='manage_college'),
    path('departments/', views.departments, name='departments'),
    path('sessions/', views.sessions, name='sessions'),
    path('sifts/', views.sifts, name='sifts'),
    path('users/', views.users, name='users'),
]