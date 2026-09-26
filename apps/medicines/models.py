from django.db import models
from django.contrib.auth.models import User
from apps.members.models import FamilyMember

class Medication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='medications')
    member = models.ForeignKey(FamilyMember, on_delete=models.CASCADE, related_name='medications')
    medicine_name = models.CharField(max_length=200)
    dosage = models.CharField(max_length=100, blank=True, null=True)
    time = models.CharField(max_length=100, blank=True, null=True, help_text="e.g., Morning, 8:00 AM, Twice Daily")
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.medicine_name} ({self.member.name})"
