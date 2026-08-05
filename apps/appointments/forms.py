from django import forms
from .models import Appointment

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['member', 'doctor_name', 'hospital', 'date', 'time', 'reason', 'status']
        widgets = {
            'member': forms.Select(attrs={'class': 'form-select'}),
            'doctor_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Dr. Name'}),
            'hospital': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Hospital / Clinic'}),
            'date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'time': forms.TimeInput(attrs={'class': 'form-input', 'type': 'time'}),
            'reason': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2, 'placeholder': 'Reason for visit'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
