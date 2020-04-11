from django.contrib.auth import login, authenticate
from django.views.generic import ListView, CreateView, DetailView, TemplateView
from django.shortcuts import redirect, render
from .models import User, Doctor, Patient, Add_appointments, Appointment
from .forms import UserSignUpForm, DoctorSignupForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils import timezone
from datetime import date
from django.core.mail import send_mail
from django.conf import settings


def index(request):
    return render(request=request, template_name='users/index.html')


class HelloTemplate(TemplateView):
    template_name = "users/book_form.html"

    def get_context_data(self, **kwargs):
        context = super(HelloTemplate, self).get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        context = {
            "slot": request.GET.get('slot'),
            "pat_name": request.GET.get('pat_name'),
            "add": request.GET.get('add'),
            "doc_name": request.GET.get('doc_name'),
            "date": request.GET.get('date'),
            "price": request.GET.get('price'),
            "clinic_name": request.GET.get('clinic_name'),
            "clinic_add": request.GET.get('clinic_add'),
            "disease": request.GET.get('disease'),
            "symp": request.GET.get('symp'),
        }

        current_user = request.user
        a = Patient.objects.get(pk=current_user.pk)

        name1 = request.GET.get('doc_name')
        sp = name1.rsplit(" ", 1)
        f = sp[0]
        l = sp[1]
        b = User.objects.filter(first_name=f, last_name=l)
        b = Doctor.objects.get(pk=b[0].pk)

        from datetime import datetime
        temp = request.GET.get('date'),

        date_input = temp[0]
        date_obj = datetime.strptime(date_input, '%B %d, %Y')
        # print (date_obj.strftime('%d/%m/%Y'))

        p = Appointment(slots=request.GET.get('slot'),
                        clinic_name=request.GET.get('clinic_name'),
                        price=request.GET.get('price'),
                        appointment_date=date_obj,
                        clinic_address=request.GET.get('clinic_add'),
                        patient_address=request.GET.get('add'),
                        disease=request.GET.get('disease'),
                        symptoms=request.GET.get('symp'),
                        patient=a,
                        doctor=b,
                        )
        p.save()
        return render(request, self.template_name, context=context)


def signup(request):
    return render(request=request, template_name='users/register.html')


def signup_patient(request):
    if request.method == 'POST':
        userform = UserSignUpForm(request.POST, prefix='userform')
        if userform.is_valid():
            user = userform.save()
            user.role = User.PATIENT
            user.date_of_birth = request.POST.get('date_of_birth')
            user.save()
            patient = Patient(user=user)
            patient.user = user
            patient.save()

            username = userform.cleaned_data.get('username')
            raw_password = userform.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)

            subject = "I'm so glad you registered on Doc-Pat"
            message = f"Hello Patient your username is {user.username} make sure you\
                 don't share your account detail because its unique for you"
            from_email = settings.EMAIL_HOST_USER
            to_list = [user.email, settings.EMAIL_HOST_USER]
            send_mail(subject, message, from_email, to_list, fail_silently=True)
            login(request, user)
            return redirect('index')
    else:
        userform = UserSignUpForm(prefix='userform')
    return render(request=request, template_name='users/register_patient.html',
                  context={'userform': userform})


def signup_doctor(request):
    if request.method == 'POST':
        userform = UserSignUpForm(request.POST, prefix='userform')
        doctorform = DoctorSignupForm(request.POST, prefix='doctorform')
        if userform.is_valid() and doctorform.is_valid():
            user = userform.save()
            user.role = User.DOCTOR
            user.date_of_birth = request.POST.get('date_of_birth')
            user.save()
            doctor = doctorform.save()
            doctor.user = user
            doctor.time_slot = 30
            doctor.save()
            username = userform.cleaned_data.get('username')
            raw_password = userform.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)

            subject = "I'm so glad you registered on Doc-Pat"
            message = f"Hello Doctor your username is {user.username} make sure you\
                 don't share your account details because its unique for you"
            from_email = settings.EMAIL_HOST_USER
            to_list = [user.email, settings.EMAIL_HOST_USER]
            send_mail(subject, message, from_email, to_list, fail_silently=True)
            login(request, user)
            return redirect('index')
    else:
        userform = UserSignUpForm(prefix='userform')
        doctorform = DoctorSignupForm(request.POST, prefix='doctorform')
    return render(request=request, template_name='users/register_doctor.html',
                  context={'userform': userform, 'doctorform': doctorform, })


class Book_app(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'users/book.html'
    context_object_name = "doc"

    # queryset = Add_appointments.objects.all()

    def get_queryset(self):
        now = timezone.now()
        upcoming = Add_appointments.objects.filter(appointment_date__gte=now).order_by('appointment_date')
        return list(upcoming)

    def get_context_data(self, **kwargs):
        now = timezone.now()
        context = super(Book_app, self).get_context_data(**kwargs)
        context['passed'] = Add_appointments.objects.filter(appointment_date__lt=now).order_by('-appointment_date')
        return context

    def test_func(self):
        if self.request.user.role == 1:
            return True
        else:
            return False


class Book_appointment(LoginRequiredMixin, DetailView):
    model = Add_appointments
    template_name = 'users/book_appointment.html'

    def get_context_data(self, **kwargs):
        li = []
        for i in range(11, 12):
            li.append([str(i) + ":00 - " + str(i) + ":30"])
            li.append([str(i) + ":30 - " + str(i + 1) + ":00"])
        for i in range(1, 6):
            li.append(["0" + str(i) + ":00 - " + "0" + str(i) + ":30"])
            li.append(["0" + str(i) + ":30 - " + "0" + str(i + 1) + ":00"])
        di = {}
        for i in li:
            t = {i[0]: i[0]}
            di.update(t)

        """context = super(Book_appointment, self).get_context_data(**kwargs)
        context['app_data'] = Appointment.objects.all()
        return context"""

        context = super(Book_appointment, self).get_context_data(**kwargs)
        context['app_data'] = di
        return context


class Show_appListView(LoginRequiredMixin, ListView):
    template_name = "users/show_app.html"
    context_object_name = "app_name"

    def get_queryset(self):
        current_user = self.request.user
        in_doc = Doctor.objects.get(pk=current_user.pk)
        now = timezone.now()
        upcoming = Appointment.objects.filter(
            doctor=in_doc, appointment_date__gte=now).order_by('appointment_date')
        return list(upcoming)

    def get_context_data(self, **kwargs):
        current_user = self.request.user
        now = timezone.now()
        in_doc = Doctor.objects.get(pk=current_user.pk)
        context = super(Show_appListView, self).get_context_data(**kwargs)
        context['passed'] = Appointment.objects.filter(doctor=in_doc, appointment_date__lt=now).order_by(
            '-appointment_date')
        return context


class Profile(LoginRequiredMixin, ListView):
    template_name = 'users/profile.html'
    context_object_name = "profile_data"
    queryset = Doctor.objects.all()


class Add_appointmentCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Add_appointments
    template_name = 'users/add_form.html'
    fields = ["clinic_name", "address", "appointment_date", "price", "appointment_time_from", "appointment_time_to", ]

    def test_func(self):
        if self.request.user.role == 2:
            return True
        else:
            return False

    def form_valid(self, form):
        my_d = Doctor.objects.get(user=self.request.user)
        form.instance.doctor_name = my_d
        return super().form_valid(form)
