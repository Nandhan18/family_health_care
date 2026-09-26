from django.db import models
from django.contrib.auth.models import User
from apps.members.models import FamilyMember

class AIPrediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ai_predictions')
    member = models.ForeignKey(FamilyMember, on_delete=models.CASCADE, related_name='ai_predictions')
    diabetes_risk = models.FloatField(default=0.0)
    heart_disease_risk = models.FloatField(default=0.0)
    hypertension_risk = models.FloatField(default=0.0)
    recommendations = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"AI Assessment for {self.member.name}"
