from django.urls import path
from home import views

urlpatterns = [
    path('', views.home, name='home'),
    path('students/', views.delete_seasson, name='delete'),
    path('find-info/', views.search_info, name='search'),
    path('save-info/', views.save_data, name='save-info'),
    path('student-info/<str:id>/', views.student, name='student'),
    path('update-info/<str:id>/', views.update_info, name='update'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('delete-student/<str:id>/', views.delete_sel, name='delete_sel')
]