from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import date, timedelta


class User(AbstractUser):
    PATIENT = 1
    DOCTOR = 2
    ROLE_CHOICES = (
        (PATIENT, 'Patient'),
        (DOCTOR, 'Doctor'),
    )
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True, default="None")
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.username


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    department = models.CharField(max_length=500)
    education = models.CharField(max_length=500)

    def __str__(self):
        return self.user.get_full_name()


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.get_full_name()


class Add_appointments(models.Model):
    clinic_name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    date_posted = models.DateTimeField(default=timezone.now)
    appointment_date = models.DateField(verbose_name=('Appointment Date: yyyy-mm-dd'))
    doctor_name = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    available_slots = models.CharField(max_length=200,default="",null=True,blank=True)

    """def save(self, *args, **kwargs):
        date_today = date.today()
        date_after_month = date_today + timedelta(days=30)
        if self.appointment_date < date.today():
            raise ValidationError("The date cannot be in the past!")
        elif self.appointment_date > date_after_month:
            raise ValidationError("the date cannot be greater than a month")
        super(Add_appointments, self).save(*args, **kwargs)"""

    def __str__(self):
        return f"{self.clinic_name} by {self.doctor_name}"


class Appointment(models.Model):

    TIMEPERIOD= (

    ('11:00 - 11:30','11:00 - 11:30'),

    ('11:30 - 12:00','11:30 - 12:00'),

    ('12:00 - 12:30','12:00 - 12:30'), 

    ('12:30 - 01:00','12:30 - 01:00'),

    ('02:00 - 02:30','02:00 - 02:30'), 

    ("02:30 - 03:00",'02:30 - 03:00'),

    ("03:00 - 03:30",'03:00 - 03:30'),

    ('03:30 - 04:00','03:30 - 04:00'), 

    ('04:30 - 05:00','04:30 - 05:00'), 

    ('05:30 - 06:00','05:30 - 06:00'),
    )

    slots = models.CharField(choices=TIMEPERIOD, max_length=200,null=True, blank=True)
    clinic_name = models.CharField(max_length=100)
    price = models.IntegerField()
    appointment_date = models.DateField()
    clinic_address = models.CharField(max_length=200)
    patient_address = models.CharField(max_length=200)
    disease = models.CharField(max_length=100)
    symptoms = models.CharField(max_length=200)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    def __str__(self):
        return self.clinic_name