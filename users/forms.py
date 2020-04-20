from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Doctor, User, Appointment
from django.forms import ModelForm, Textarea
import re
class UserSignUpForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter username'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter your first name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter your last name'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'}))
    password1 = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}))
    password2 = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            #self.fields['username'].widget.attrs['class'] = 'form-control validate'
            self.fields[field].widget.attrs.update({
                'class': 'validate'
            })


class DoctorSignupForm(forms.ModelForm):
    education = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'eductaion'}))
    department = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'department'}))

    class Meta:
        model = Doctor
        fields = ('education', 'department')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'validate'
            })
"""

class Book_appointmentForm(forms.ModelForm):
    class meta:
        model = Appointment
        fields = ('patient_address', 'disease', 'patient', 'symptoms', 'doctor')
"""