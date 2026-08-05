from django import forms
from .models import Medication

class MedicationForm(forms.ModelForm):
    class Meta:
        model = Medication
        fields = ['member', 'medicine_name', 'dosage', 'time', 'start_date', 'end_date']
        widgets = {
            'member': forms.Select(attrs={'class': 'form-select'}),
            'medicine_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Medicine Name (e.g. Paracetamol)'}),
            'dosage': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Dosage (e.g. 500mg)'}),
            'time': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Frequency / Time (e.g. Morning, Night)'}),
            'start_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
        }
