from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from apps.members.models import FamilyMember
from .models import MedicalRecord
from .forms import MedicalRecordForm
from .utils import generate_health_summary_pdf

@login_required
def medical_records_view(request):
    user_members = FamilyMember.objects.filter(user=request.user)
    if request.method == 'POST':
        form = MedicalRecordForm(request.POST, request.FILES)
        form.fields['member'].queryset = user_members
        if form.is_valid():
            record = form.save(commit=False)
            record.user = request.user
            record.save()
            messages.success(request, "Medical record uploaded successfully.")
            return redirect('medical_records')
        else:
            messages.error(request, "Error uploading medical record. Please check form inputs.")
    else:
        form = MedicalRecordForm()
        form.fields['member'].queryset = user_members
    
    records = MedicalRecord.objects.filter(user=request.user).select_related('member').order_by('-date_uploaded')
    return render(request, 'medical_records.html', {'records': records, 'form': form})

@login_required
def delete_medical_record(request, pk):
    record = get_object_or_404(MedicalRecord, pk=pk, user=request.user)
    record.delete()
    messages.success(request, "Medical record deleted.")
    return redirect('medical_records')

@login_required
def export_pdf_view(request, member_id=None):
    pdf_bytes = generate_health_summary_pdf(request.user, member_id=member_id)
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    filename = f"Family_Health_Passport_{request.user.username}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response
