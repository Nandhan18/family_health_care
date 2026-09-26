from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from apps.members.models import FamilyMember
from apps.records.models import MedicalRecord
from apps.medicines.models import Medication
from apps.appointments.models import Appointment
from .forms import CustomUserCreationForm

def landing_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'landing.html')

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome to Family Care, {user.first_name}! Your account has been created.")
            return redirect('dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'auth/signup.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'auth/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')

@login_required
def dashboard_view(request):
    members_count = FamilyMember.objects.filter(user=request.user).count()
    records_count = MedicalRecord.objects.filter(user=request.user).count()
    medicines_count = Medication.objects.filter(user=request.user).count()
    appointments_count = Appointment.objects.filter(user=request.user, status='Scheduled').count()

    recent_appointments = Appointment.objects.filter(user=request.user).select_related('member').order_by('-date')[:3]
    recent_records = MedicalRecord.objects.filter(user=request.user).select_related('member').order_by('-date_uploaded')[:3]

    context = {
        'members_count': members_count,
        'records_count': records_count,
        'medicines_count': medicines_count,
        'appointments_count': appointments_count,
        'recent_appointments': recent_appointments,
        'recent_records': recent_records,
    }
    return render(request, 'dashboard.html', context)
