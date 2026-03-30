import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elearning_project.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
username = 'superadmin'
email = 'admin@example.com'
password = 'superadmin@123'

# Delete existing user to be sure
User.objects.filter(username=username).delete()

# Create superuser with correct role
user = User.objects.create_superuser(username, email, password)
user.role = 'superadmin'
user.save()

print(f"User {username} created successfully with role 'superadmin'.")
