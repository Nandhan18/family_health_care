from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from datetime import date, timedelta

from apps.members.models import FamilyMember
from apps.records.models import MedicalRecord
from apps.medicines.models import Medication
from apps.appointments.models import Appointment
from apps.analytics.models import HealthMetric
from apps.predictions.models import AIPrediction

class Command(BaseCommand):
    help = 'Seed demo data for Family Care application'

    def handle(self, *args, **options):
        self.stdout.write("Seeding Family Care demo data...")

        # Create or update demo user
        user, created = User.objects.get_or_create(username='demo', defaults={'email': 'demo@familycare.local'})
        if created:
            user.set_password('demo1234')
            user.save()
            self.stdout.write(self.style.SUCCESS("Created demo user: username 'demo', password 'demo1234'"))

        # Create admin user if not exists
        admin_user, admin_created = User.objects.get_or_create(username='admin', defaults={'email': 'admin@familycare.local', 'is_staff': True, 'is_superuser': True})
        if admin_created:
            admin_user.set_password('admin1234')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS("Created admin user: username 'admin', password 'admin1234'"))

        # Family Members
        m1, _ = FamilyMember.objects.get_or_create(
            user=user, name='John Doe',
            defaults={
                'relation': 'Self', 'age': 42, 'gender': 'Male', 'blood_group': 'O+',
                'allergies': 'Penicillin', 'chronic_conditions': 'Mild Seasonal Asthma',
                'emergency_contact': '+1 (555) 234-5678'
            }
        )
        m2, _ = FamilyMember.objects.get_or_create(
            user=user, name='Jane Doe',
            defaults={
                'relation': 'Spouse', 'age': 39, 'gender': 'Female', 'blood_group': 'A+',
                'allergies': 'Dust Mites', 'chronic_conditions': 'None',
                'emergency_contact': '+1 (555) 234-5678'
            }
        )
        m3, _ = FamilyMember.objects.get_or_create(
            user=user, name='Leo Doe',
            defaults={
                'relation': 'Son', 'age': 12, 'gender': 'Male', 'blood_group': 'O+',
                'allergies': 'Peanuts', 'chronic_conditions': 'None',
                'emergency_contact': '+1 (555) 234-5678'
            }
        )
        m4, _ = FamilyMember.objects.get_or_create(
            user=user, name='Martha Doe',
            defaults={
                'relation': 'Mother', 'age': 68, 'gender': 'Female', 'blood_group': 'B+',
                'allergies': 'Sulfa drugs', 'chronic_conditions': 'Hypertension, Osteoarthritis',
                'emergency_contact': '+1 (555) 987-6543'
            }
        )

        # Medical Records
        MedicalRecord.objects.get_or_create(
            user=user, member=m1, record_type='Lab Result',
            defaults={'notes': 'Annual Lipid Panel & Blood Glucose: All parameters within normal ranges.', 'date_uploaded': date.today() - timedelta(days=15)}
        )
        MedicalRecord.objects.get_or_create(
            user=user, member=m4, record_type='Doctor Note',
            defaults={'notes': 'Cardiology consultation: BP controlled at 128/82. Continue current dosage of Lisinopril.', 'date_uploaded': date.today() - timedelta(days=5)}
        )
        MedicalRecord.objects.get_or_create(
            user=user, member=m3, record_type='Vaccination Record',
            defaults={'notes': 'Annual Influenza booster vaccine administered.', 'date_uploaded': date.today() - timedelta(days=30)}
        )

        # Medications
        Medication.objects.get_or_create(
            user=user, member=m4, medicine_name='Lisinopril',
            defaults={'dosage': '10mg', 'time': 'Morning after breakfast', 'start_date': date.today() - timedelta(days=180)}
        )
        Medication.objects.get_or_create(
            user=user, member=m1, medicine_name='Omega-3 Fish Oil',
            defaults={'dosage': '1000mg', 'time': 'Once daily with meals', 'start_date': date.today() - timedelta(days=60)}
        )
        Medication.objects.get_or_create(
            user=user, member=m3, medicine_name='Cetirizine Syrup',
            defaults={'dosage': '5ml', 'time': 'As needed for allergies', 'start_date': date.today() - timedelta(days=10)}
        )

        # Appointments
        Appointment.objects.get_or_create(
            user=user, member=m4, doctor_name='Sarah Jenkins',
            defaults={'hospital': 'City Heart Institute', 'date': date.today() + timedelta(days=7), 'time': '10:30:00', 'reason': 'Quarterly Blood Pressure & Heart Checkup', 'status': 'Scheduled'}
        )
        Appointment.objects.get_or_create(
            user=user, member=m3, doctor_name='Robert Chen',
            defaults={'hospital': 'Sunnyside Pediatrics Clinic', 'date': date.today() + timedelta(days=14), 'time': '14:00:00', 'reason': 'Growth & School Physical Examination', 'status': 'Scheduled'}
        )

        # Health Metrics
        HealthMetric.objects.get_or_create(
            user=user, member=m4, record_date=date.today() - timedelta(days=2),
            defaults={'blood_pressure': '128/82', 'sugar_level': 108.5, 'weight': 64.2}
        )
        HealthMetric.objects.get_or_create(
            user=user, member=m1, record_date=date.today() - timedelta(days=1),
            defaults={'blood_pressure': '118/78', 'sugar_level': 92.0, 'weight': 78.5}
        )

        # AI Predictions
        AIPrediction.objects.get_or_create(
            user=user, member=m4,
            defaults={'diabetes_risk': 18.5, 'heart_disease_risk': 22.0, 'hypertension_risk': 34.5, 'recommendations': 'Maintain low-sodium dietary intake, moderate 30-minute daily morning walks, and monitor resting blood pressure weekly.'}
        )
        AIPrediction.objects.get_or_create(
            user=user, member=m1,
            defaults={'diabetes_risk': 7.2, 'heart_disease_risk': 5.8, 'hypertension_risk': 11.4, 'recommendations': 'Excellent overall health indicators. Continue regular physical exercise and balanced nutrition.'}
        )

        self.stdout.write(self.style.SUCCESS("Successfully seeded Family Care database!"))
