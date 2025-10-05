"""
Management command to create initial superuser if none exists
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Creates an initial superuser if no users exist'

    def handle(self, *args, **options):
        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write(self.style.SUCCESS('Superuser already exists'))
            return

        # Create superuser with default credentials
        # CHANGE THESE AFTER FIRST LOGIN!
        User.objects.create_superuser(
            username='admin',
            email='admin@stmarysnyakhobi.ac.ke',
            password='StMarys2025!Change'  # Change this after first login!
        )
        
        self.stdout.write(self.style.SUCCESS(
            'Successfully created superuser: admin\n'
            'Password: StMarys2025!Change\n'
            'IMPORTANT: Change this password immediately after first login!'
        ))
