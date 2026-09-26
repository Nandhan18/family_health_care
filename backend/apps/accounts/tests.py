from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from apps.members.models import FamilyMember
from apps.medicines.models import Medication
from apps.appointments.models import Appointment
from apps.analytics.models import HealthMetric

class FamilyCareModularTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.member = FamilyMember.objects.create(
            user=self.user,
            name='Jane Doe',
            relation='Spouse',
            age=35,
            gender='Female',
            blood_group='A+'
        )

    def test_landing_page(self):
        response = self.client.get(reverse('landing'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'All Your Family’s Medical Records')

    def test_family_member_creation(self):
        self.assertEqual(str(self.member), 'Jane Doe (Spouse)')
        self.assertEqual(self.member.age, 35)

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_dashboard_authenticated(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testuser')

    def test_family_members_list(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('family_members'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Jane Doe')

    def test_add_medication(self):
        self.client.login(username='testuser', password='password123')
        med = Medication.objects.create(
            user=self.user,
            member=self.member,
            medicine_name='Vitamin C',
            dosage='500mg'
        )
        response = self.client.get(reverse('medicines'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Vitamin C')

    def test_add_appointment(self):
        self.client.login(username='testuser', password='password123')
        appnt = Appointment.objects.create(
            user=self.user,
            member=self.member,
            doctor_name='Smith',
            date='2026-09-01'
        )
        response = self.client.get(reverse('appointments'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Dr. Smith')

    def test_health_vitals_logging_and_deletion(self):
        self.client.login(username='testuser', password='password123')
        metric = HealthMetric.objects.create(
            user=self.user,
            member=self.member,
            blood_pressure='120/80',
            sugar_level=95.0,
            weight=65.0
        )
        response = self.client.get(reverse('health_analytics'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '120/80')

        # Test deletion
        del_response = self.client.get(reverse('delete_health_metric', kwargs={'pk': metric.pk}))
        self.assertEqual(del_response.status_code, 302)
        self.assertFalse(HealthMetric.objects.filter(pk=metric.pk).exists())

    def test_export_pdf_report(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('export_health_pdf'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertTrue(response.content.startswith(b'%PDF'))
