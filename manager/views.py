from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from home.models import StudentSaf
from django.contrib.auth.models import User
from . models import Institute, Year, Department, Shift, Semester
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def auth(request):
    if request.user.is_superuser:
        return redirect('manage_college')
    elif request.user.is_authenticated and not request.user.is_superuser:
        messages.warning(request, 'You are not allowed to access admin panel')
        return redirect('delete')
    elif request.user.is_authenticated and request.user.is_superuser:
        return redirect('manage_college')
    else:
        return redirect('auth_login')

def auth_login(request):
    """User login"""
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('manage_college')
        else:
            return redirect('delete')
    # if not request.user.is_superuser:
    #     messages.error(request, 'Your are not allowed to Admin panel!')
        # return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_authenticated and not user.is_superuser:
                login(request, user)
                messages.success(request, 'Welcome back! Logged in as User.')
                return redirect('delete')  # Redirect to 'delete' page if login is successful
            elif user.is_authenticated and user.is_superuser:
                login(request, user)
                messages.success(request, 'Welcome back! Logged in as Super user.')
                return redirect('manage_college')
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
    institute = Institute.objects.all().first()
    context = {
        'page': 'Login SAF Admin',
        'students_count': students_count,
        'institute': institute
    }
    return render(request, 'home/login.html', context)


def auth_create(request):
    if not request.user.is_superuser:
        messages.error(request, 'Your are not allowed to Admin panel!')
        return redirect('home')
    """User create"""
    referal_url = request.META.get('HTTP_REFERER', request.path_info)
    if not request.user.is_authenticated:
        messages.warning(request, 'Please Login first')
        return redirect('auth_login')
    students_count = StudentSaf.objects.all().count()
    institute = Institute.objects.all().first()
    context = {
        'page': 'Create SAF Admin',
        'students_count': students_count,
        'institute': institute
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

@csrf_exempt
def institute(request):
    """TODO: Show institute"""
    if not request.user.is_superuser:
        messages.error(request, 'Your are not allowed to Admin panel!')
        return redirect('home')
    referal_url = request.META.get('HTTP_REFERER', request.path_info)
    if not request.user.is_superuser:
        
        return HttpResponseRedirect(referal_url)
    
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
    # students_count = StudentSaf.objects.all.count()
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

@csrf_exempt
def departments(request):
    if not request.user.is_superuser:
        messages.error(request, 'Your are not allowed to Admin panel!')
        return redirect('home')
    referal_url = request.META.get('HTTP_REFERER', request.path_info)
    departments = Department.objects.all()
    assigned_users = Department.objects.values_list('head', flat=True)
    users = User.objects.filter(is_staff=True, is_active=True, is_superuser=False).exclude(id__in=assigned_users)
    students_count = StudentSaf.objects.all().count()
    institute = Institute.objects.all().first()
    context = {
        'page': 'Departments',
        'departments': departments,
        'users': users,
        'students_count': students_count,
        'institute': institute
    }
    if request.method == 'POST':
        department_name = request.POST.get('department_name', '').strip()
        head_of_dep = request.POST.get('head_of_dep', '').strip()

        try:
            user_obj = User.objects.get(id=head_of_dep)
            department_obj = Department.objects.filter(name=department_name).first()

            if department_obj:
                messages.error(request, 'Department already exists in the system')
                return HttpResponseRedirect(referal_url)
            if not user_obj:
                messages.error(request, 'Invalid User')
            
            department = Department.objects.create(
                name=department_name,
                head=user_obj
            )
            if department:
                messages.success(request, 'Department Created Succesfully')
            
            return HttpResponseRedirect(referal_url)

        except Exception as e:
            print(e)
            return HttpResponseRedirect(referal_url)

    return render(request, 'home/departments.html', context)

def delete_department(request, uid):
    if not request.user.is_superuser:
        messages.error(request, 'Your are not allowed to Admin panel!')
        return redirect('home')
    referal_url = request.META.get('HTTP_REFERER', request.path_info)
    try:
        department_obj = Department.objects.get(uid=uid)
        if department_obj:
            department_obj.delete()
            messages.warning(request, 'Department has been deleted successfully!')
    except Exception as e:
        print(e)
    return HttpResponseRedirect(referal_url)

@csrf_exempt
def years(request):
    if not request.user.is_superuser:
        messages.error(request, 'Your are not allowed to Admin panel!')
        return redirect('home')
    referal_url = request.META.get('HTTP_REFERER', request.path_info)
    years = Year.objects.all()
    students_count = StudentSaf.objects.all().count()
    institute = Institute.objects.all().first()
    context = {
        'page': 'Sessions',
        'sessions': years,
        'institute': institute,
        'students_count': students_count
    }

    if request.method == 'POST':
        try:
            year_session = request.POST.get('session', '').strip()
            session_year = request.POST.get('session_year', '').strip()

            # Correct usage of get_or_create
            get_session, created = Year.objects.get_or_create(
                session=year_session,  # This field is used for lookup
                defaults={'year': session_year}  # This field is only used if a new object is created
            )

            if created:
                messages.success(request, 'Session created successfully!')
            else:
                messages.warning(request, 'Session already exists.')

            return HttpResponseRedirect(referal_url)

        except Exception as e:
            print("Error:", e)
            messages.error(request, "An error occurred while creating the session.")

    return render(request, 'home/sessions.html', context)

def delete_year(request, id):
    if not request.user.is_superuser:
        messages.error(request, 'Your are not allowed to Admin panel!')
        return redirect('home')
    referal_url = request.META.get('HTTP_REFERER', request.path_info)
    try:
        year_obj = Year.objects.get(id=id)

        if year_obj:
            year_obj.delete()
            messages.success(request, 'Session deleted successfully')
    except Exception as e:
        print(e)
    return HttpResponseRedirect(referal_url)

@csrf_exempt
def sifts(request):
    if not request.user.is_superuser:
        messages.error(request, 'Your are not allowed to Admin panel!')
        return redirect('home')
    referal_url = request.META.get('HTTP_REFERER', request.path_info)
    shifts = Shift.objects.all()
    context = {
        'page': 'Shifts',
        'shifts': shifts
    }
    if request.method == 'POST':
        try:
            shift = request.POST.get('shift', '').strip()
            group = request.POST.get('group', '').strip()

            Shift.objects.create(
                shift=shift,
                group=group
            )
            messages.success(request, 'Shift Created successfully! ')
            
        except Exception as e:
            print(e)
        return HttpResponseRedirect(referal_url)
    students_count = StudentSaf.objects.all().count()
    institute = Institute.objects.all().first()
    context.update({
        'institute': institute,
        'students_count': students_count
    })

    return render(request, 'home/sifts.html', context)

def delete_shift(request, uid):
    if not request.user.is_superuser:
        messages.error(request, 'Your are not allowed to Admin panel!')
        return redirect('home')
    referal_url = request.META.get('HTTP_REFERER', request.path_info)
    shift_obj = Shift.objects.get(uid=uid)
    if shift_obj:
        shift_obj.delete()
        messages.success(request, 'Shift deleted successfully!')
    else:
        messages.error(request, 'No Shift exists!')
    return HttpResponseRedirect(referal_url)

@csrf_exempt
def users(request):
    if not request.user.is_superuser:
        messages.error(request, 'Your are not allowed to Admin panel!')
        return redirect('home')
    if not request.user.is_superuser or not request.user.is_authenticated:
        return redirect('auth_login')
    referal_url = request.META.get('HTTP_REFERER', request.path_info)
    users = User.objects.filter(is_staff=True,is_superuser=False).order_by('id')
    context = {
        'page': 'Users',
        'users': users
    }

    if request.method == 'POST':
        try:
            name = request.POST.get('name').strip()
            email = request.POST.get('email').strip()
            password = request.POST.get('password').strip()

            user_obj, created = User.objects.get_or_create(
                defaults={
                    'username':email
                },
                first_name=name,
                email=email,
                is_active=True,
                is_staff=True,
                is_superuser= False
            )
            if created: 
                user_obj.set_password(password)
                user_obj.save()
                messages.success(request, 'User created successfully')
                return HttpResponseRedirect(referal_url)
            else:
                messages.warning(request, 'User already exists.')
                return HttpResponseRedirect(referal_url)
        except Exception as e:
            print(e)
            return HttpResponseRedirect(referal_url)
    students_count = StudentSaf.objects.all().count()
    institute = Institute.objects.all().first()
    context.update({
        'institute': institute,
        'students_count': students_count
    })

    return render(request, 'home/users.html', context)

def delete_user(request, username):
    if not request.user.is_superuser:
        messages.error(request, 'Your are not allowed to Admin panel!')
        return redirect('home')
    referal_url = request.META.get('HTTP_REFERER', request.path_info)
    context = {
        'page': 'Delete User',
    }

    try:
        user_obj = User.objects.filter(username=username).first()
        if user_obj:
            user_obj.delete()
            messages.success(request, 'User deleted successfully!')
            return HttpResponseRedirect(referal_url)
        else:
            messages.warning(request, 'No User found.')
            return HttpResponseRedirect(referal_url)
    except Exception as e:
        print(e)

    return HttpResponseRedirect(referal_url)


def semesters(request):
    if not request.user.is_superuser:
        messages.warning(request, 'You are not allowed to access Admin Panel')
        return redirect('home')
    referal_url = request.META.get('HTTP_REFERER', request.path_info)
    semesters = Semester.objects.all().order_by('name')
    context = {
        'page': 'Semesters',
        'semesters': semesters
    }
    if request.method == 'POST':
        try:
            name = request.POST.get('name', '').strip()
            created = Semester.objects.create(name=name)
            if created:
                messages.success(request, 'Semester created Successfully!')
            else:
                messages.error(request, 'Semester already exists!')
        except Exception as e:
            print(e)
        return HttpResponseRedirect(referal_url)
    students_count = StudentSaf.objects.all().count()
    institute = Institute.objects.all().first()
    context.update({
        'institute': institute,
        'students_count': students_count
    })
    return render(request, 'home/semesters.html', context)


def delete_semester(request, uid):
    if not request.user.is_superuser:
        messages.warning(request, 'You are not allowed to access Admin Panel')
        return redirect('home')
    referal_url = request.META.get('HTTP_REFERER', request.path_info)
    semester_obj = Semester.objects.get(uid=uid)
    if semester_obj is not None:
        semester_obj.delete()
    return HttpResponseRedirect(referal_url)