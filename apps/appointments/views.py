from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.members.models import FamilyMember
from .models import Appointment
from .forms import AppointmentForm

@login_required
def appointments_view(request):
    user_members = FamilyMember.objects.filter(user=request.user)
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        form.fields['member'].queryset = user_members
        if form.is_valid():
            appnt = form.save(commit=False)
            appnt.user = request.user
            appnt.save()
            messages.success(request, f"Appointment scheduled with Dr. {appnt.doctor_name}.")
            return redirect('appointments')
        else:
            messages.error(request, "Error scheduling appointment. Please check form inputs.")
    else:
        form = AppointmentForm()
        form.fields['member'].queryset = user_members
    
    appointments = Appointment.objects.filter(user=request.user).select_related('member').order_by('date')
    return render(request, 'appointments.html', {'appointments': appointments, 'form': form})

@login_required
def delete_appointment(request, pk):
    appnt = get_object_or_404(Appointment, pk=pk, user=request.user)
    appnt.delete()
    messages.success(request, "Appointment cancelled.")
    return redirect('appointments')
