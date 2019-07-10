from django.db import models
from django.conf import settings
# Create your models here.
User = settings.AUTH_USER_MODEL

class UserProfile(models.Model):
	
	user = models.ForeignKey(User,null=True,on_delete=models.SET_NULL)
	image = models.ImageField(upload_to='image/',blank=True,null=True)
	position = models.CharField(max_length=35,null=True)
	content = models.TextField(null=True, blank=True)