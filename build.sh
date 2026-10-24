#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate


python manage.py shell << END
from django.contrib.auth import get_user_model
from bookings.models import Service
User = get_user_model()
import os

username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'Admin@12345')

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print("Superuser created successfully.")

if not Service.objects.exists():
    Service.objects.create(name="Standard Consultation", duration_minutes=30, price=500.00, is_active=True)
    Service.objects.create(name="Express Verification", duration_minutes=15, price=250.00, is_active=True)
    print("Demo services seeded.")
END