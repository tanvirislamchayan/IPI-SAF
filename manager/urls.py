from django.urls import path
from . import views

urlpatterns = [
    path('', views.auth, name='auth'),
    path('login/', views.auth_login, name='auth_login'),
    path('create/', views.auth_create, name='auth_create'),
    path('institute/', views.institute, name='manage_college'),
    path('departments/', views.departments, name='departments'),
    path('departments/delete/<str:uid>', views.delete_department, name='delete_department'),
    path('sessions/', views.years, name='sessions'),
    path('sessions/delete/<str:id>', views.delete_year, name='delete_session'),
    path('sifts/', views.sifts, name='sifts'),
    path('shift/delete/<str:uid>', views.delete_shift, name='delete_shift' ),
    path('users/', views.users, name='users'),
    path('users/delete/<str:username>', views.delete_user, name='delete_user'),
]