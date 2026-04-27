import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'noorani_backend.settings')
django.setup()

from django.contrib.auth.models import User

username = 'shaban'
password = 'shaban@123'
email = 'shaban@example.com'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f"Superuser '{username}' was created successfully!")
else:
    print(f"Superuser '{username}' already exists.")
