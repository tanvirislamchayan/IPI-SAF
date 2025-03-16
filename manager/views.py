from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from home.models import StudentSaf
from django.contrib.auth.models import User
from . models import Institute

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
    """TODO: Show institute"""
    referal_url = request.META.get('HTTP_REFERER', request.path_info)
    
    if not request.user.is_authenticated and not request.user.is_superuser:
        messages.warning(request, 'Please Login first')
        return redirect('auth_login')

    students_count = StudentSaf.objects.all().count()
    
    if request.method == 'POST':
        institute_name_bn = request.POST.get('institute_name_bn', '').strip()
        institute_logo = request.FILES.get('institute_logo', None)  # Ensure correct handling of file input
        institute_address_bn = request.POST.get('institute_address_bn', '').strip()
        institute_code = request.POST.get('institute_code', '').strip()
        contact_number_1 = request.POST.get('contact_number_1', '').strip()
        contact_number_2 = request.POST.get('contact_number_2', '').strip()

        # Get existing institute:
        institute_obj = Institute.objects.all().first()
        if not institute_obj:
            institute_obj = Institute.objects.create(
                institute_name_bn='JS Polytechnic'
            )
        institute_obj.institute_name_bn=institute_name_bn
        institute_obj.institute_address_bn=institute_address_bn
        institute_obj.institute_code=institute_code
        institute_obj.contact_number_1=contact_number_1
        institute_obj.contact_number_2=contact_number_2
        institute_obj.save()
        if institute_logo:
            institute_obj.institute_logo=institute_logo
            institute_obj.save()
        

        
        return HttpResponseRedirect(referal_url)
    institute_obj = Institute.objects.all().first()
    if not institute_obj:
        institute_obj = Institute.objects.create(
            institute_name_bn='JS Polytechnic Institute'
        )
    context = {
        'page': 'Manage College',
        'students_count': students_count,
        'institute': institute_obj
    }
    
    return render(request, 'home/manage_college.html', context)


def departments(request):
    return render(request, 'home/departments.html')


def sessions(request):
    return render(request, 'home/sessions.html')

def sifts(request):
    return render(request, 'home/sifts.html')


def users(request):
    return render(request, 'home/users.html')