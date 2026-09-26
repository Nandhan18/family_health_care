from django import forms
from .models import HealthMetric

class HealthMetricForm(forms.ModelForm):
    class Meta:
        model = HealthMetric
        fields = ['member', 'blood_pressure', 'sugar_level', 'weight', 'record_date']
        widgets = {
            'member': forms.Select(attrs={'class': 'form-select'}),
            'blood_pressure': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. 120/80'}),
            'sugar_level': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Fasting / Post-meal (mg/dL)'}),
            'weight': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Weight (kg)'}),
            'record_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
        }
