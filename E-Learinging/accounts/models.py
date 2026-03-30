from django.contrib.auth.models import AbstractUser
from django.db import models
from college.models import College

class User(AbstractUser):
    ROLE_CHOICES = (
        ('superadmin', 'Super Admin'),
        ('admin', 'Admin'),
        ('faculty', 'Faculty'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    college = models.ForeignKey(College, on_delete=models.CASCADE, null=True, blank=True, related_name='users')
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
