from django.shortcuts import render, redirect
from authorize.forms import singupform
from django.contrib.auth import login
from django.urls import reverse
from patient.models import patient
import datetime

def frontpage(request):
    return render(request, 'authorize/frontpage.html')

def homepage(request):
    userPatient = patient.objects.filter(doctor = request.user)
    now = datetime.date.today()

    appointment = []
    for item in userPatient:
        if item.appointment > now:
            appointment.append(item.appointment)

    if not appointment:
        closest_date = 0
        patientName = "None"
    else:
        date_differ = [abs(date-now) for date in appointment]

        closest_date = appointment[date_differ.index(min(date_differ))]
        patientName = userPatient.get(appointment = closest_date)

    context = {'date':closest_date, 'pt_name': patientName, 'applist':userPatient}

    return render(request, 'authorize/homepage.html', context)

def signup(request):
    if request.method == 'GET':
        return render(
            request, "authorize/signup.html",
            {"form": singupform}
        )
    elif request.method == 'POST':
        form = singupform(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("homepage")

def test(request):
    return render(request, 'authorize/test.html')