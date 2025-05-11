import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MainWeb.settings")
django.setup()

from django.contrib.auth.models import User

username = "admin"
email = "admin@example.com"
password = "adminpassword123"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print("✅ Superuser created.")
else:
    print("⚠️ Superuser already exists.")
