from django.db import models

# Create your models here.

class Enrolled_Course(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.CharField(max_length=200)
    image = models.ImageField(upload_to='course_images/', null=True, blank=True)
    user = models.CharField(max_length=20)
    
    