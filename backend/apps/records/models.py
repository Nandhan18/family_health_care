from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from apps.members.models import FamilyMember

class MedicalRecord(models.Model):
    RECORD_TYPES = [
        ('Lab Result', 'Lab Result'),
        ('Prescription', 'Prescription'),
        ('Doctor Note', 'Doctor Note'),
        ('Imaging', 'Imaging / X-Ray'),
        ('Vaccination', 'Vaccination Record'),
        ('Other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='medical_records')
    member = models.ForeignKey(FamilyMember, on_delete=models.CASCADE, related_name='medical_records')
    record_type = models.CharField(max_length=50, choices=RECORD_TYPES, default='Lab Result')
    notes = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='medical_records/', blank=True, null=True)
    ocr_text = models.TextField(blank=True, null=True)
    date_uploaded = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.record_type} for {self.member.name} - {self.date_uploaded}"
