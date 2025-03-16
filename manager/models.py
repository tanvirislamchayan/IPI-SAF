import os
from django.db import models
from django.core.files.storage import default_storage

class Institute(models.Model):
    institute_name_bn = models.CharField(max_length=155, null=True, blank=True)
    institute_logo = models.ImageField(upload_to='institute_logos/', null=True, blank=True)
    institute_address_bn = models.CharField(max_length=255, null=True, blank=True)
    institute_code = models.CharField(max_length=50, unique=True, null=True, blank=True)
    contact_number_1 = models.CharField(max_length=20, null=True, blank=True)
    contact_number_2 = models.CharField(max_length=20, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Check if instance already exists in the database
        if self.pk:
            existing_institute = Institute.objects.filter(pk=self.pk).first()
            if existing_institute and existing_institute.institute_logo and self.institute_logo != existing_institute.institute_logo:
                # Delete the old logo file if a new one is being uploaded
                if default_storage.exists(existing_institute.institute_logo.name):
                    default_storage.delete(existing_institute.institute_logo.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.institute_name_bn if self.institute_name_bn else "Unnamed Institute"

"""season/year"""
class Year(models.Model):
    year = models.CharField(max_length=10, unique=True)

    def __str__(self) -> str:
        return self.year
    
    