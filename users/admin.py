from django.contrib import admin
from . models import User, Doctor, Patient, Appointment, Add_appointments

admin.site.register(User)
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Appointment)
admin.site.register(Add_appointments)