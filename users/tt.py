from models import User, Doctor, Patient, Add_appointments,Appointment
aa=Appointment.objects.all()

for i in aa:
    print(i)
    #print(Appointment.objects.filter(doctor=i.doctor)
