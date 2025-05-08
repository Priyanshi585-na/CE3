from django.db import models
import uuid
from django.contrib.auth.models import User

class UserProfile(models.Model):
    id = models.CharField(primary_key=True,default=uuid.uuid4,editable=False,max_length=40)
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    profile_image = models.ImageField(upload_to='users/',blank=True, null=True)
