from django.contrib import admin
from .models import AIPrediction

@admin.register(AIPrediction)
class AIPredictionAdmin(admin.ModelAdmin):
    list_display = ('member', 'diabetes_risk', 'heart_disease_risk', 'hypertension_risk', 'created_at')
