from django.urls import path
from . import views as user_views
from django.contrib.auth import views as auth_views
from .views import (Book_app,
                    Book_appointment,
                    Profile,
                    Add_appointmentCreateView,
                    HelloTemplate,
                    Show_appListView)


urlpatterns = [

    path('', user_views.index, name="index"),

    path('register/', user_views.signup, name='register'),

    path('register_as_patient/', user_views.signup_patient, name='register_patient'),

    path('register_as_doctor/', user_views.signup_doctor, name='register_doctor'),

    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name="login"),

    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name="logout"),

    path('profile/', Profile.as_view(), name='profile'),

    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='users/password_reset.html'),
         name="password_reset"),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'),
         name="password_reset_done"),

    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name="password_reset_confirm"),

    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'),
         name="password_reset_complete"),

    path('book/', Book_app.as_view(), name='book'),

    path('book/book_appointment/<int:pk>/', Book_appointment.as_view(), name='book_appointment'),

    path('book/book_appointment/<int:pk>/book_form/', HelloTemplate.as_view(), name='book_form'),

    path('add_appointment/', Add_appointmentCreateView.as_view(success_url="/",), name='add_form'),

    path('show_app/', Show_appListView.as_view(), name='show_app'),

]
