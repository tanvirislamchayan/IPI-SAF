from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from home.models import StudentSaf
from django.contrib.auth.models import User

# Create your views here.

def auth_login(request):
    """User login"""
    if request.user.is_authenticated:
        return redirect('delete')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_authenticated:
                login(request, user)
                return redirect('delete')  # Redirect to 'delete' page if login is successful
            else:
                # Handle the case where the user is not a superuser
                context = {
                    'page': 'Login SAF Admin',
                    'error': 'You are not authorized to access this page.'
                }
                messages.warning(request, 'You are not authorized to access this page.')
                return HttpResponseRedirect(request.path_info)
        else:
            # Handle invalid login credentials
            context = {
                'page': 'Login SAF Admin',
                'error': 'Invalid username or password.'
            }
            messages.warning(request, 'Invalid username or password.')
            return HttpResponseRedirect(request.path_info)
    students_count = StudentSaf.objects.all().count()
    
    context = {
        'page': 'Login SAF Admin',
        'students_count': students_count
    }
    return render(request, 'home/login.html', context)


def auth_create(request):
    """User create"""
    referal_url = request.META.get('HTTP_REFERER', request.path_info)
    if not request.user.is_authenticated:
        messages.warning(request, 'Please Login first')
        return redirect('auth_login')
    students_count = StudentSaf.objects.all().count()
    context = {
        'page': 'Create SAF Admin',
        'students_count': students_count
    }

    if request.method == 'POST':
        try:
            first_name = request.POST.get('first_name', '').strip()
            last_name = request.POST.get('last_name', '').strip()
            email = request.POST.get('email', '').strip()
            password = request.POST.get('password', '').strip()
            confirm_password = request.POST.get('confirm_password', '').strip()

            if password != confirm_password:
                return HttpResponseRedirect(referal_url)
            
            user_obj, created = User.objects.get_or_create(
                defaults={
                    'username': email
                },
                email=email,
                first_name=first_name,
                last_name=last_name
            )
            if created:
                user_obj.set_password(password)
                messages.success(request, 'User created successfully')
                return redirect('home')
        except Exception as e:
            print(e)
    
    return render(request, 'home/user_create.html', context)


def institute(request):
    referal_url = request.META.get('HTTP_REFERER', request.path_info)
    if not request.user.is_authenticated and not request.user.is_superuser:
        messages.warning(request, 'Please Login first')
        return redirect('auth_login')
    students_count = StudentSaf.objects.all().count()
    context = {
        'page': 'Manage College',
        'students_count': students_count
    }

    return render(request, 'home/manage_college.html', context)