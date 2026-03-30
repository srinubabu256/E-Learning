from django.db import models
from django.conf import settings
from college.models import Branch, Year

class Course(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='courses', null=True)
    year = models.ForeignKey(Year, on_delete=models.CASCADE, related_name='courses', null=True)
    faculty = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'role': 'faculty'})
    created_at = models.DateTimeField(auto_now_add=True)
    thumbnail = models.ImageField(upload_to='courses/', null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.branch.name} - {self.year.year})"

class Enrollment(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.course.name}"
