from django.db import models
from django.contrib.auth.models import User
from apps.members.models import FamilyMember

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Scheduled', 'Scheduled'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    member = models.ForeignKey(FamilyMember, on_delete=models.CASCADE, related_name='appointments')
    doctor_name = models.CharField(max_length=150)
    hospital = models.CharField(max_length=200, blank=True, null=True)
    date = models.DateField()
    time = models.TimeField(blank=True, null=True)
    reason = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Scheduled')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Dr. {self.doctor_name} with {self.member.name} on {self.date}"
