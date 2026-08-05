from django import forms
from .models import FamilyMember

class FamilyMemberForm(forms.ModelForm):
    class Meta:
        model = FamilyMember
        fields = ['name', 'relation', 'age', 'gender', 'blood_group', 'allergies', 'chronic_conditions', 'emergency_contact']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Full Name'}),
            'relation': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Spouse, Father'}),
            'age': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Age'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'blood_group': forms.Select(attrs={'class': 'form-select'}),
            'allergies': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2, 'placeholder': 'Any known allergies'}),
            'chronic_conditions': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2, 'placeholder': 'Pre-existing conditions'}),
            'emergency_contact': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Phone / Contact details'}),
        }
