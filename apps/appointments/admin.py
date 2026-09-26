from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('doctor_name', 'member', 'hospital', 'date', 'status', 'user')
    list_filter = ('status', 'date')
