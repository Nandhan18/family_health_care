from django.contrib import admin
from .models import Medication

@admin.register(Medication)
class MedicationAdmin(admin.ModelAdmin):
    list_display = ('medicine_name', 'member', 'dosage', 'time', 'user')
