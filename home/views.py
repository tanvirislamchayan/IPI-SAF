from django.shortcuts import render, redirect
from .models import  StudentSaf, PaymentSystem
from allstudents.models import AllStudent
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.contrib import messages
from django.urls import reverse
from django.core.files.storage import default_storage
from django.contrib.auth import authenticate, login, logout
import os
from django.db.models import Q

from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from manager.models import Institute, Year, Shift, Department, Semester


# Create your views here.


def home(request):
    institute = Institute.objects.all().first()
    students_count = StudentSaf.objects.all().count()
    years = Year.objects.all().order_by('year')
    shifts = Shift.objects.all()
    departments = Department.objects.all().order_by('name')
    semesters = Semester.objects.all().order_by('name')
    # all_students = AllStudent.objects.last()
    # if all_students:
    #     all_students.check_validity()
    context = {
        'page':'Home',
        'years': years,
        'students_count': students_count,
        'institute': institute,
        'departments': departments,
        'shifts': shifts,
        'semesters': semesters,
    }
    return render(request, 'home/home.html', context=context)



def save_data(request):
    referal_url = request.META.get('HTTP_REFERER', request.path_info)
    # all_students = AllStudent.objects.last()
    # if all_students:
    #     all_students.check_validity()
    if request.method == 'POST':

        """Personal info"""
        # Student info
        name = request.POST.get('name').strip()
        nameEng = request.POST.get('nameEng').strip()
        birthCertNo = request.POST.get('birthCertNumber').strip()
        dob = request.POST.get('dob').strip()
        sex = request.POST.get('sex').strip()

        # Father's info
        fatherName = request.POST.get('fatherName').strip()
        fatherNameEng = request.POST.get('fatherNameEng').strip()
        fatherNID = request.POST.get('fatherNID').strip()
        fatherDob = request.POST.get('fatherDob').strip()
        fatherMobile = request.POST.get('fatherMobile').strip()

        # Mother's info
        motherName = request.POST.get('motherName').strip()
        motherNameEng = request.POST.get('motherNameEng').strip()
        motherNID = request.POST.get('motherNID').strip()
        motherDob = request.POST.get('motherDob').strip()
        motherMobile = request.POST.get('motherMobile').strip()

        """Address"""
        # Present Address
        presentDiv = request.POST.get('presentDivision').strip()
        presentDist = request.POST.get('presentDistrict').strip()
        presentUpozila = request.POST.get('presentUpozila').strip()
        presentUnion = request.POST.get('presentUnion').strip()
        presentPost = request.POST.get('presentPost').strip()
        presentVill = request.POST.get('presentVillage').strip()

        # permanent Address
        permanentDiv = request.POST.get('permanentDivision').strip()
        permanentDist = request.POST.get('permanentDistrict').strip()
        permanentUpozila = request.POST.get('permanentUpozila').strip()
        permanentUnion = request.POST.get('permanentUnion').strip()
        permanentPost = request.POST.get('permanentPost').strip()
        permanentVill = request.POST.get('permanentVillage').strip()


        """Educational Qualification"""
        # Previous Qualification
        prevEduDivi = request.POST.get('prevEduDivision').strip()
        prevEduDist = request.POST.get('prevEduDistrict').strip()
        prevEduUpozila = request.POST.get('prevEduUpozila').strip()
        prevEduInst = request.POST.get('prevEduInstitute').strip()
        prevEduBoard = request.POST.get('prevEduBoard').strip()
        prevEduPassYear = request.POST.get('prevEduPassYear').strip()
        prevEduTech = request.POST.get('prevEduTechnology').strip()
        prevEduExam = request.POST.get('prevEduExamName').strip()
        prevEduRoll = request.POST.get('prevEduRoll').strip()
        prevEduReg = request.POST.get('prevEduRegistration').strip()
        prevEduResult = request.POST.get('prevEduResult').strip()

        # Present Qualification
        presentEduDivi = request.POST.get('presentEduDivision').strip()
        presentEduDist = request.POST.get('presentEduDistrict').strip()
        presentEduUpozila = request.POST.get('presentEduUpozila').strip()
        presentEduInstitute = request.POST.get('presentEduInstitute').strip()
        presentEduSem = request.POST.get('presentEduSemester').strip()
        presentEduTech = request.POST.get('presentEduTechnology', '').strip()
        presentEduShift = request.POST.get('presentEduShift').strip()
        presentEduSession = request.POST.get('presentEduSession').strip()
        presentEduRoll = request.POST.get('presentEduRoll').strip()

        """guardian Info"""
        guardian = request.POST.get('guardian').strip()
        guardianName = request.POST.get('guardianName').strip()
        guardianNameEng = request.POST.get('guardianNameEng').strip()
        guardianNID = request.POST.get('guardianNID').strip()
        guardianDob = request.POST.get('guardianDob').strip()
        guardianMobile = request.POST.get('guardianMobile').strip()

        """Eligibility Conditions and Attachment"""
        eduCostBearer = request.POST.get('eduCostBearer').strip()
        freedomFighter = request.POST.get('freedomFighter').strip()
        protibondhi = request.POST.get('protibondhi').strip()
        nrigosti = request.POST.get('nrigosti').strip()
        otherScholar = request.POST.get('otherScholarSource').strip()

        """Attachments/Images"""
        applicantPhoto = request.FILES.get('applicantPhoto')
        documents = request.FILES.get('documents')


        """Payment System"""
        # student
        paymentAccountName = request.POST.get('paymentAccountName').strip()
        paymentAccountNID = request.POST.get('paymentAccountNID').strip()
        paymentType = request.POST.get('paymentType').strip()
        paymentAccountNo = request.POST.get('paymentAccountNumber').strip()
        paymentMobileBankName = request.POST.get('paymentMobileBankName').strip()
        paymentBankName = request.POST.get('paymentBankName').strip()
        paymentBankBranch = request.POST.get('paymentBankBranch').strip()
        bankAccountType = request.POST.get('bankAccountType')

        semester_obj = Semester.objects.get(uid=presentEduSem)
        if semester_obj is None:
            messages.error(request, "Semeste doesn't exists!!")
            return HttpResponseRedirect(referal_url)
        
        department_obj = Department.objects.get(uid=presentEduTech)
        if department_obj is None:
            messages.error(request, "Semester doesn't exists")
            return HttpResponseRedirect(referal_url)
        
        shift_obj = Shift.objects.get(uid=presentEduShift)
        if shift_obj is None:
            messages.error(request, "Shift doesn't exists!")
            return HttpResponseRedirect(referal_url)
       

        year_obj = Year.objects.get(id=presentEduSession)
        if year_obj is None:
            messages.error(request, "Year (Session) doesn't exists!")
            return HttpResponseRedirect(referal_url)
        
        student_exist = StudentSaf.objects.filter(presentEduRoll=presentEduRoll).first()

        if student_exist:
            messages.warning(request, "This account already exists! Please search and edit if any update needed!")
            return redirect('home')
        
        student_obj = StudentSaf.objects.create(
            name=name,
            nameEng=nameEng,
            birthCertNo=birthCertNo,
            dob=dob,
            sex=sex,
            fatherName=fatherName,
            fatherNameEng=fatherNameEng,
            fatherNID=fatherNID,
            fatherDob=fatherDob,
            fatherMobile=fatherMobile,
            motherName=motherName,
            motherNameEng=motherNameEng,
            motherNID=motherNID,
            motherDob=motherDob,
            motherMobile=motherMobile,
            presentDiv=presentDiv,
            presentDist=presentDist,
            presentUpozila=presentUpozila,
            presentUnion=presentUnion,
            presentPost=presentPost,
            presentVill=presentVill,
            permanentDiv=permanentDiv,
            permanentDist=permanentDist,
            permanentUpozila=permanentUpozila,
            permanentUnion=permanentUnion,
            permanentPost=permanentPost,
            permanentVill=permanentVill,
            prevEduDivi=prevEduDivi,
            prevEduDist=prevEduDist,
            prevEduUpozila=prevEduUpozila,
            prevEduInst=prevEduInst,
            prevEduBoard=prevEduBoard,
            prevEduPassYear=prevEduPassYear,
            prevEduTech=prevEduTech,
            prevEduExam=prevEduExam,
            prevEduRoll=prevEduRoll,
            prevEduReg=prevEduReg,
            prevEduResult=prevEduResult,
            presentEduDivi=presentEduDivi,
            presentEduDist=presentEduDist,
            presentEduUpozila=presentEduUpozila,
            presentEduInstitute=presentEduInstitute,
            presentEduSem=semester_obj,
            presentEduTech=department_obj,
            presentEduShift=shift_obj,
            presentEduSession=year_obj,  # ForeignKey reference to Year object
            presentEduRoll=presentEduRoll,
            guardian=guardian,
            guardianName=guardianName,
            guardianNameEng=guardianNameEng,
            guardianNID=guardianNID,
            guardianDob=guardianDob,
            guardianMobile=guardianMobile,
            eduCostBearer=eduCostBearer,
            freedomFighter=freedomFighter,
            protibondhi=protibondhi,
            nrigosti=nrigosti,
            otherScholar=otherScholar,
            applicantPhoto=applicantPhoto,
            documents=documents
        )

        payment_obj = PaymentSystem.objects.create(
            student=student_obj,  # ForeignKey to StudentSaf
            paymentAccountName=paymentAccountName,
            paymentAccountNID=paymentAccountNID,
            paymentType=paymentType,
            paymentAccountNo=paymentAccountNo,
            paymentMobileBankName=paymentMobileBankName,
            paymentBankName=paymentBankName,
            paymentBankBranch=paymentBankBranch,
            bankAccountType=bankAccountType
        )

    messages.success(request, 'Registered successfully!')

                
    return redirect('home')


def search_info(request):
    # all_students = AllStudent.objects.last()
    # if all_students:
    #     all_students.check_validity()
    students_count = StudentSaf.objects.all().count()
    context = {
        'page': 'Apply for SAF',
        'students_count': students_count
    }

    if request.method == 'POST':
        roll = request.POST.get('roll')
        accountNumber = request.POST.get('accountNumber')

        student_obj = StudentSaf.objects.filter(prevEduRoll=roll, studentPayment__paymentAccountNo=accountNumber).first()
        if not student_obj:
            messages.warning(request, "No Student found! Please check again")
            return HttpResponseRedirect(request.path_info)
        # Redirect to the student view with the student's id
        return redirect('student', id=student_obj.id)

    return render(request, 'search/search.html', context)

# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib import messages

def student(request, id):
    students_count = StudentSaf.objects.all().count()
    institute = Institute.objects.all().first()

    context = {
        'page': 'Apply for SAF',
        'students_count': students_count,
        'institute': institute
    }

    # all_students = AllStudent.objects.last()
    # if all_students:
    #     all_students.check_validity()

    try:
        student_obj = StudentSaf.objects.get(id=id)
        print(student_obj)
    except StudentSaf.DoesNotExist:
        messages.warning(request, 'Student not found.')
        return redirect('search')

    try:
        payment = PaymentSystem.objects.get(student_id=student_obj.id)
    except PaymentSystem.DoesNotExist:
        messages.warning(request, 'Payment information not found for this student.')
        return redirect('search')

    context.update({
        'student': student_obj,
        'payment': payment,
    })

    return render(request, 'search/student.html', context)



# update
def update_info(request, id):
    # Retrieve existing StudentSaf and PaymentSystem objects
    try:

        student_obj = StudentSaf.objects.get(id=id)
        
        # all_students = AllStudent.objects.last()
        # if all_students:
        #     all_students.check_validity()
        payment = PaymentSystem.objects.get(student_id=student_obj.id)
        years = Year.objects.all().order_by('-year')

        if request.method == 'POST':
            """Personal info"""
            # Student info
            student_obj.name = request.POST.get('name').strip()
            student_obj.nameEng = request.POST.get('nameEng').strip()
            student_obj.birthCertNo = request.POST.get('birthCertNumber').strip()
            student_obj.dob = request.POST.get('dob').strip()
            student_obj.sex = request.POST.get('sex').strip()

            # Father's info
            student_obj.fatherName = request.POST.get('fatherName').strip()
            student_obj.fatherNameEng = request.POST.get('fatherNameEng').strip()
            student_obj.fatherNID = request.POST.get('fatherNID').strip()
            student_obj.fatherDob = request.POST.get('fatherDob').strip()
            student_obj.fatherMobile = request.POST.get('fatherMobile').strip()

            # Mother's info
            student_obj.motherName = request.POST.get('motherName').strip()
            student_obj.motherNameEng = request.POST.get('motherNameEng').strip()
            student_obj.motherNID = request.POST.get('motherNID').strip()
            student_obj.motherDob = request.POST.get('motherDob').strip()
            student_obj.motherMobile = request.POST.get('motherMobile').strip()

            """Address"""
            # Present Address
            student_obj.presentDiv = request.POST.get('presentDivision').strip()
            student_obj.presentDist = request.POST.get('presentDistrict').strip()
            student_obj.presentUpozila = request.POST.get('presentUpozila').strip()
            student_obj.presentUnion = request.POST.get('presentUnion').strip()
            student_obj.presentPost = request.POST.get('presentPost').strip()
            student_obj.presentVill = request.POST.get('presentVillage').strip()

            # Permanent Address
            student_obj.permanentDiv = request.POST.get('permanentDivision').strip()
            student_obj.permanentDist = request.POST.get('permanentDistrict').strip()
            student_obj.permanentUpozila = request.POST.get('permanentUpozila').strip()
            student_obj.permanentUnion = request.POST.get('permanentUnion').strip()
            student_obj.permanentPost = request.POST.get('permanentPost').strip()
            student_obj.permanentVill = request.POST.get('permanentVillage').strip()

            """Educational Qualification"""
            # Previous Qualification
            student_obj.prevEduDivi = request.POST.get('prevEduDivision').strip()
            student_obj.prevEduDist = request.POST.get('prevEduDistrict').strip()
            student_obj.prevEduUpozila = request.POST.get('prevEduUpozila').strip()
            student_obj.prevEduInst = request.POST.get('prevEduInstitute').strip()
            student_obj.prevEduBoard = request.POST.get('prevEduBoard').strip()
            student_obj.prevEduPassYear = request.POST.get('prevEduPassYear').strip()
            student_obj.prevEduTech = request.POST.get('prevEduTechnology').strip()
            student_obj.prevEduExam = request.POST.get('prevEduExamName').strip()
            student_obj.prevEduRoll = request.POST.get('prevEduRoll').strip()
            student_obj.prevEduReg = request.POST.get('prevEduRegistration').strip()
            student_obj.prevEduResult = request.POST.get('prevEduResult').strip()

            # Present Qualification
            student_obj.presentEduDivi = request.POST.get('presentEduDivision').strip()
            student_obj.presentEduDist = request.POST.get('presentEduDistrict').strip()
            student_obj.presentEduUpozila = request.POST.get('presentEduUpozila').strip()
            student_obj.presentEduInstitute = request.POST.get('presentEduInstitute').strip()
            student_obj.presentEduSem = Semester.objects.get(uid=request.POST.get('presentEduSemester').strip())
            student_obj.presentEduTech = Department.objects.get(uid=request.POST.get('presentEduTechnology').strip())
            student_obj.presentEduShift = Shift.objects.get(uid=request.POST.get('presentEduShift').strip())
            student_obj.presentEduSession = Year.objects.get(id=request.POST.get('presentEduSession'))
            student_obj.presentEduRoll = request.POST.get('presentEduRoll').strip()

            """Guardian Info"""
            student_obj.guardian = request.POST.get('guardian').strip()
            student_obj.guardianName = request.POST.get('guardianName').strip()
            student_obj.guardianNameEng = request.POST.get('guardianNameEng').strip()
            student_obj.guardianNID = request.POST.get('guardianNID').strip()
            student_obj.guardianDob = request.POST.get('guardianDob').strip()
            student_obj.guardianMobile = request.POST.get('guardianMobile').strip()

            """Eligibility Conditions and Attachment"""
            student_obj.eduCostBearer = request.POST.get('eduCostBearer').strip()
            student_obj.freedomFighter = request.POST.get('freedomFighter').strip()
            student_obj.protibondhi = request.POST.get('protibondhi').strip()
            student_obj.nrigosti = request.POST.get('nrigosti').strip()
            student_obj.otherScholar = request.POST.get('otherScholarSource')

            """Attachments/Images"""
            # Check if a new applicantPhoto is uploaded
            if 'applicantPhoto' in request.FILES:
                if student_obj.applicantPhoto:
                    # Delete the old applicantPhoto file
                    if default_storage.exists(student_obj.applicantPhoto.path):
                        default_storage.delete(student_obj.applicantPhoto.path)
                student_obj.applicantPhoto = request.FILES['applicantPhoto']

            # Check if a new documents file is uploaded
            if 'documents' in request.FILES:
                if student_obj.documents:
                    # Delete the old documents file
                    if default_storage.exists(student_obj.documents.path):
                        default_storage.delete(student_obj.documents.path)
                student_obj.documents = request.FILES['documents']

            student_obj.save()

            """Payment System"""
            payment.paymentAccountName = request.POST.get('paymentAccountName')
            payment.paymentAccountNID = request.POST.get('paymentAccountNID')
            payment.paymentType = request.POST.get('paymentType')
            payment.paymentAccountNo = request.POST.get('paymentAccountNumber')
            payment.paymentMobileBankName = request.POST.get('paymentMobileBankName')
            payment.paymentBankName = request.POST.get('paymentBankName')
            payment.paymentBankBranch = request.POST.get('paymentBankBranch')
            payment.bankAccountType = request.POST.get('bankAccountType')
            payment.save()

            messages.success(request, 'Updated successfully!')
            return redirect('student', id=student_obj.id)
        students_count = StudentSaf.objects.all().count()
        semesters = Semester.objects.all().order_by('name')
        shifts = Shift.objects.all()
        departments = Department.objects.all().order_by('name')
        institute = Institute.objects.all().first()
        context = {
            'page': 'IPI | Update Info for SAF',
            'student': student_obj,
            'payment': payment,
            'years': years,
            'students_count': students_count,
            'semesters': semesters,
            'shifts': shifts,
            'departments': departments,
            'institute': institute,
        }
        return render(request, 'search/update.html', context)
    
    except StudentSaf.DoesNotExist:
        # Return 'no student found' with status 204
        return HttpResponse("No student found", status=204)






def delete_seasson(request):
    # Check if the user is a superuser
    if not request.user.is_authenticated:
        messages.warning(request, 'Please Login first.')
        return redirect('login')
    
    seassons = Year.objects.all().order_by('-year')
    students = StudentSaf.objects.all().order_by('-id')
    if 'search' in request.GET:
        search_term = request.GET.get('search', '').strip()
        students = students.filter(
                        Q(nameEng__icontains=search_term) |
                        Q(name__icontains=search_term) |
                        Q(prevEduRoll__icontains=search_term) |
                        Q(presentEduRoll__icontains=search_term) |
                        Q(studentPayment__paymentAccountNo__icontains=search_term)
                    )
    # all_students = AllStudent.objects.last()
    # if all_students:
    #     all_students.check_validity()
    
    selected_seasson = ''
    if 'seasson' in request.GET:
        seasson = request.GET.get('seasson')
        selected_seasson = seasson
        students = StudentSaf.objects.filter(presentEduSession__year=seasson)
    
    if request.method == "POST":
        selected_ids = request.POST.getlist('selection')
        print(selected_ids)  # Debugging print statement
        for student_id in selected_ids:
            try:
                student = StudentSaf.objects.get(id=student_id)
                
                # Delete the images and documents associated with the student
                if student.applicantPhoto and default_storage.exists(student.applicantPhoto.path):
                    default_storage.delete(student.applicantPhoto.path)
                        
                if student.documents and default_storage.exists(student.documents.path):
                    default_storage.delete(student.documents.path)
                
                # Delete the student record
                student.delete()
                
            except StudentSaf.DoesNotExist:
                pass

        # Redirect to the referring page to avoid resubmission on refresh
        referer_url = request.META.get('HTTP_REFERER', 'delete')  # Fallback to 'delete' if no referer
        return HttpResponseRedirect(referer_url)
    students_count = StudentSaf.objects.all().count()

    context = {
        'page': 'Students SAF | IPI',
        'seassons': seassons,
        'students': students,
        'selected_seasson': selected_seasson,
        'students_count': students_count
    }
    return render(request, 'home/delete.html', context)




def user_login(request):
    # all_students = AllStudent.objects.last()
    # if all_students:
    #     all_students.check_validity()
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
                    'page': 'Login SAF Admin | API',
                    'error': 'You are not authorized to access this page.'
                }
                messages.warning(request, 'You are not authorized to access this page.')
                return HttpResponseRedirect(request.path_info)
        else:
            # Handle invalid login credentials
            context = {
                'page': 'Login SAF Admin | API',
                'error': 'Invalid username or password.'
            }
            messages.warning(request, 'Invalid username or password.')
            return HttpResponseRedirect(request.path_info)
    students_count = StudentSaf.objects.all().count()
    
    context = {
        'page': 'Login SAF Admin | API',
        'students_count': students_count
    }
    return render(request, 'home/login.html', context)





def user_logout(request):
    # all_students = AllStudent.objects.last()
    # if all_students:
    #     all_students.check_validity()
    logout(request)
    return redirect('login') 


def delete_sel(request, id):
    if not request.user.is_authenticated:
        messages.warning(request, 'Please Login first.')
        return redirect('login')
    student_obj = StudentSaf.objects.get(id=id)
    student_obj.delete()
    return redirect('delete')