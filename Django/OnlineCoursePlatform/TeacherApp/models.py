from django.db import models
import uuid

class Course(models.Model):
    id = models.CharField(primary_key=True,default=uuid.uuid4,editable=False,max_length=40)
    course_image = models.FileField(upload_to='course_images/')
    course_videos = models.FileField(upload_to='course_videos/')
    is_draft = models.BooleanField(default=False)
    enrolled = models.BooleanField(default=False)
