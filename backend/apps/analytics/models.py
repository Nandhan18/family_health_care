from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from apps.members.models import FamilyMember

class HealthMetric(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='health_metrics')
    member = models.ForeignKey(FamilyMember, on_delete=models.CASCADE, related_name='health_metrics')
    blood_pressure = models.CharField(max_length=20, blank=True, null=True, help_text="e.g. 120/80")
    sugar_level = models.FloatField(blank=True, null=True, help_text="mg/dL")
    weight = models.FloatField(blank=True, null=True, help_text="kg")
    record_date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Vitals for {self.member.name} on {self.record_date}"
