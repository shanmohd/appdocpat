from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include('users.urls')),

]

"""path('', user_views.index, name="index"),

   path('register/', user_views.signup, name='register'),

   path('registeraspatient/', user_views.signup_patient, name='register_patient'),

   path('registerasdoctor/', user_views.signup_doctor, name='register_doctor'),

   path('book/', Book_app.as_view(), name='book'),

   path('book/book_appointment/', user_views.book_appointment, name='book_appointment'),"""