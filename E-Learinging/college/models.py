from django.db import models

class College(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def total_courses(self):
        from courses.models import Course
        return Course.objects.filter(branch__college=self).count()

class Branch(models.Model):
    name = models.CharField(max_length=100)
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name='branches')

    def __str__(self):
        return f"{self.name} ({self.college.name})"

class Year(models.Model):
    year = models.CharField(max_length=10) # e.g. 1st, 2nd, 3rd, 4th

    def __str__(self):
        return self.year
