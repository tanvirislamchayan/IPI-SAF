from django.shortcuts import render, redirect
from .models import Year, StudentSaf, PaymentSystem
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
from manager.models import Institute


# Create your views here.


def home(request):
    institute = Institute.objects.all().first()
    students_count = StudentSaf.objects.all().count()
    years = Year.objects.all().order_by('-year')
    # all_students = AllStudent.objects.last()
    # if all_students:
    #     all_students.check_validity()
    context = {
        'page':'Home',
        'years': years,
        'students_count': students_count,
        'institute': institute
    }
    return render(request, 'home/home.html', context=context)



def save_data(request):
    # all_students = AllStudent.objects.last()
    # if all_students:
    #     all_students.check_validity()
    if request.method == 'POST':

        """Personal info"""
        # Student info
        name = request.POST.get('name')
        nameEng = request.POST.get('nameEng')
        birthCertNo = request.POST.get('birthCertNumber')
        dob = request.POST.get('dob')
        sex = request.POST.get('sex')

        # Father's info
        fatherName = request.POST.get('fatherName')
        fatherNameEng = request.POST.get('fatherNameEng')
        fatherNID = request.POST.get('fatherNID')
        fatherDob = request.POST.get('fatherDob')
        fatherMobile = request.POST.get('fatherMobile')

        # Mother's info
        motherName = request.POST.get('motherName')
        motherNameEng = request.POST.get('motherNameEng')
        motherNID = request.POST.get('motherNID')
        motherDob = request.POST.get('motherDob')
        motherMobile = request.POST.get('motherMobile')

        """Address"""
        # Present Address
        presentDiv = request.POST.get('presentDivision')
        presentDist = request.POST.get('presentDistrict')
        presentUpozila = request.POST.get('presentUpozila')
        presentUnion = request.POST.get('presentUnion')
        presentPost = request.POST.get('presentPost')
        presentVill = request.POST.get('presentVillage')

        # permanent Address
        permanentDiv = request.POST.get('permanentDivision')
        permanentDist = request.POST.get('permanentDistrict')
        permanentUpozila = request.POST.get('permanentUpozila')
        permanentUnion = request.POST.get('permanentUnion')
        permanentPost = request.POST.get('permanentPost')
        permanentVill = request.POST.get('permanentVillage')


        """Educational Qualification"""
        # Previous Qualification
        prevEduDivi = request.POST.get('prevEduDivision')
        prevEduDist = request.POST.get('prevEduDistrict')
        prevEduUpozila = request.POST.get('prevEduUpozila')
        prevEduInst = request.POST.get('prevEduInstitute')
        prevEduBoard = request.POST.get('prevEduBoard')
        prevEduPassYear = request.POST.get('prevEduPassYear')
        prevEduTech = request.POST.get('prevEduTechnology')
        prevEduExam = request.POST.get('prevEduExamName')
        prevEduRoll = request.POST.get('prevEduRoll')
        prevEduReg = request.POST.get('prevEduRegistration')
        prevEduResult = request.POST.get('prevEduResult')

        # Present Qualification
        presentEduDivi = request.POST.get('presentEduDivision')
        presentEduDist = request.POST.get('presentEduDistrict')
        presentEduUpozila = request.POST.get('presentEduUpozila')
        presentEduInstitute = request.POST.get('presentEduInstitute')
        presentEduSem = request.POST.get('presentEduSemester')
        presentEduTech = request.POST.get('presentEduTechnology')
        presentEduShift = request.POST.get('presentEduShift')
        presentEduSession = request.POST.get('presentEduSession')
        presentEduRoll = request.POST.get('presentEduRoll')

        """guardian Info"""
        guardian = request.POST.get('guardian')
        guardianName = request.POST.get('guardianName')
        guardianNameEng = request.POST.get('guardianNameEng')
        guardianNID = request.POST.get('guardianNID')
        guardianDob = request.POST.get('guardianDob')
        guardianMobile = request.POST.get('guardianMobile')

        """Eligibility Conditions and Attachment"""
        eduCostBearer = request.POST.get('eduCostBearer')
        freedomFighter = request.POST.get('freedomFighter')
        protibondhi = request.POST.get('protibondhi')
        nrigosti = request.POST.get('nrigosti')
        otherScholar = request.POST.get('otherScholarSource')

        """Attachments/Images"""
        applicantPhoto = request.FILES.get('applicantPhoto')
        documents = request.FILES.get('documents')


        """Payment System"""
        # student
        paymentAccountName = request.POST.get('paymentAccountName')
        paymentAccountNID = request.POST.get('paymentAccountNID')
        paymentType = request.POST.get('paymentType')
        paymentAccountNo = request.POST.get('paymentAccountNumber')
        paymentMobileBankName = request.POST.get('paymentMobileBankName')
        paymentBankName = request.POST.get('paymentBankName')
        paymentBankBranch = request.POST.get('paymentBankBranch')
        bankAccountType = request.POST.get('bankAccountType')

        year_obj = Year.objects.get(year=presentEduSession)
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
            presentEduSem=presentEduSem,
            presentEduTech=presentEduTech,
            presentEduShift=presentEduShift,
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
        'page': 'IPI | Apply for SAF',
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

    context = {
        'page': 'IPI | Apply for SAF',
        'students_count': students_count
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
            student_obj.name = request.POST.get('name')
            student_obj.nameEng = request.POST.get('nameEng')
            student_obj.birthCertNo = request.POST.get('birthCertNumber')
            student_obj.dob = request.POST.get('dob')
            student_obj.sex = request.POST.get('sex')

            # Father's info
            student_obj.fatherName = request.POST.get('fatherName')
            student_obj.fatherNameEng = request.POST.get('fatherNameEng')
            student_obj.fatherNID = request.POST.get('fatherNID')
            student_obj.fatherDob = request.POST.get('fatherDob')
            student_obj.fatherMobile = request.POST.get('fatherMobile')

            # Mother's info
            student_obj.motherName = request.POST.get('motherName')
            student_obj.motherNameEng = request.POST.get('motherNameEng')
            student_obj.motherNID = request.POST.get('motherNID')
            student_obj.motherDob = request.POST.get('motherDob')
            student_obj.motherMobile = request.POST.get('motherMobile')

            """Address"""
            # Present Address
            student_obj.presentDiv = request.POST.get('presentDivision')
            student_obj.presentDist = request.POST.get('presentDistrict')
            student_obj.presentUpozila = request.POST.get('presentUpozila')
            student_obj.presentUnion = request.POST.get('presentUnion')
            student_obj.presentPost = request.POST.get('presentPost')
            student_obj.presentVill = request.POST.get('presentVillage')

            # Permanent Address
            student_obj.permanentDiv = request.POST.get('permanentDivision')
            student_obj.permanentDist = request.POST.get('permanentDistrict')
            student_obj.permanentUpozila = request.POST.get('permanentUpozila')
            student_obj.permanentUnion = request.POST.get('permanentUnion')
            student_obj.permanentPost = request.POST.get('permanentPost')
            student_obj.permanentVill = request.POST.get('permanentVillage')

            """Educational Qualification"""
            # Previous Qualification
            student_obj.prevEduDivi = request.POST.get('prevEduDivision')
            student_obj.prevEduDist = request.POST.get('prevEduDistrict')
            student_obj.prevEduUpozila = request.POST.get('prevEduUpozila')
            student_obj.prevEduInst = request.POST.get('prevEduInstitute')
            student_obj.prevEduBoard = request.POST.get('prevEduBoard')
            student_obj.prevEduPassYear = request.POST.get('prevEduPassYear')
            student_obj.prevEduTech = request.POST.get('prevEduTechnology')
            student_obj.prevEduExam = request.POST.get('prevEduExamName')
            student_obj.prevEduRoll = request.POST.get('prevEduRoll')
            student_obj.prevEduReg = request.POST.get('prevEduRegistration')
            student_obj.prevEduResult = request.POST.get('prevEduResult')

            # Present Qualification
            student_obj.presentEduDivi = request.POST.get('presentEduDivision')
            student_obj.presentEduDist = request.POST.get('presentEduDistrict')
            student_obj.presentEduUpozila = request.POST.get('presentEduUpozila')
            student_obj.presentEduInstitute = request.POST.get('presentEduInstitute')
            student_obj.presentEduSem = request.POST.get('presentEduSemester')
            student_obj.presentEduTech = request.POST.get('presentEduTechnology')
            student_obj.presentEduShift = request.POST.get('presentEduShift')
            student_obj.presentEduSession = Year.objects.get(year=request.POST.get('presentEduSession'))
            student_obj.presentEduRoll = request.POST.get('presentEduRoll')

            """Guardian Info"""
            student_obj.guardian = request.POST.get('guardian')
            student_obj.guardianName = request.POST.get('guardianName')
            student_obj.guardianNameEng = request.POST.get('guardianNameEng')
            student_obj.guardianNID = request.POST.get('guardianNID')
            student_obj.guardianDob = request.POST.get('guardianDob')
            student_obj.guardianMobile = request.POST.get('guardianMobile')

            """Eligibility Conditions and Attachment"""
            student_obj.eduCostBearer = request.POST.get('eduCostBearer')
            student_obj.freedomFighter = request.POST.get('freedomFighter')
            student_obj.protibondhi = request.POST.get('protibondhi')
            student_obj.nrigosti = request.POST.get('nrigosti')
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
        context = {
            'page': 'IPI | Update Info for SAF',
            'student': student_obj,
            'payment': payment,
            'years': years,
            'students_count': students_count
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