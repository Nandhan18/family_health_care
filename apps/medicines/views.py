from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.members.models import FamilyMember
from .models import Medication
from .forms import MedicationForm

@login_required
def medicines_view(request):
    user_members = FamilyMember.objects.filter(user=request.user)
    if request.method == 'POST':
        form = MedicationForm(request.POST)
        form.fields['member'].queryset = user_members
        if form.is_valid():
            med = form.save(commit=False)
            med.user = request.user
            med.save()
            messages.success(request, f"Medication '{med.medicine_name}' added.")
            return redirect('medicines')
        else:
            messages.error(request, "Error adding medication. Please check form inputs.")
    else:
        form = MedicationForm()
        form.fields['member'].queryset = user_members
    
    medicines = Medication.objects.filter(user=request.user).select_related('member').order_by('-created_at')
    return render(request, 'medicines.html', {'medicines': medicines, 'form': form})

@login_required
def delete_medicine(request, pk):
    med = get_object_or_404(Medication, pk=pk, user=request.user)
    med.delete()
    messages.success(request, "Medication removed.")
    return redirect('medicines')
