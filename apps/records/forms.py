from django import forms
from .models import MedicalRecord

class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ['member', 'record_type', 'notes', 'file']
        widgets = {
            'member': forms.Select(attrs={'class': 'form-select'}),
            'record_type': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3, 'placeholder': 'Doctor observations, notes, etc.'}),
            'file': forms.FileInput(attrs={'class': 'form-file'}),
        }
