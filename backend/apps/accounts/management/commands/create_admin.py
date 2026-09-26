from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Create or reset an administrator account with custom credentials'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, default='admin', help='Admin Username')
        parser.add_argument('--email', type=str, default='admin@familycare.local', help='Admin Email')
        parser.add_argument('--password', type=str, default='admin1234', help='Admin Password')

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']

        user, created = User.objects.get_or_create(
            username=username,
            defaults={'email': email, 'is_staff': True, 'is_superuser': True}
        )

        user.email = email
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()

        if created:
            self.stdout.write(self.style.SUCCESS(f"Successfully created Admin user: '{username}' with password '{password}'"))
        else:
            self.stdout.write(self.style.SUCCESS(f"Successfully updated Admin user: '{username}' with new password '{password}'"))
