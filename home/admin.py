from django.contrib import admin
from .models import StudentSaf, PaymentSystem, Year, AllStudent

# Register your models here.
admin.site.register(StudentSaf)
admin.site.register(PaymentSystem)
admin.site.register(AllStudent)
admin.site.register(Year)