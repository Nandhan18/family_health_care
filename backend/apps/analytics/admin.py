from django.contrib import admin
from .models import HealthMetric

@admin.register(HealthMetric)
class HealthMetricAdmin(admin.ModelAdmin):
    list_display = ('member', 'blood_pressure', 'sugar_level', 'weight', 'record_date', 'user')
