from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse
from taggit.managers import TaggableManager
User = settings.AUTH_USER_MODEL

# Create your models here.

class Post(models.Model):
	user = models.ForeignKey(User,default=1,null=True,on_delete=models.SET_NULL)
	title = models.CharField(max_length=90,null=True)
	image = models.ImageField(upload_to='image/',blank=True,null=True)
	content = models.TextField(null=True,blank=False)
	timestamp = models.DateTimeField(auto_now=False,auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	votes = models.IntegerField(default=0)
	total_answers = models.IntegerField(default=0)
	tags = TaggableManager(blank=True)

	class Meta:
		ordering = ['-updated','-timestamp']

	def get_absolute_url(self):
		return reverse("post:post-detail", kwargs={"id": self.id})

	def __str__(self):
		return '%s' % (self.title)

class Answer(models.Model):
	post = models.ForeignKey(Post,null=True,on_delete=models.SET_NULL)
	user = models.ForeignKey(User,default=1,null=True,on_delete=models.SET_NULL)
	image = models.ImageField(upload_to='image/',blank=True,null=True)
	content = models.TextField()
	timestamp = models.DateTimeField(auto_now=False,auto_now_add=True)
	votes = models.IntegerField(default=0)
	is_accepted = models.BooleanField(default=False)

class Comment(models.Model):
	post = models.ForeignKey(Post,null=True,on_delete=models.SET_NULL)
	answer = models.ForeignKey(Answer,null=True,on_delete=models.SET_NULL)
	user = models.ForeignKey(User,default=1,null=True,on_delete=models.SET_NULL)
	content = models.TextField(null=True,blank=False)
	timestamp = models.DateTimeField(auto_now=False,auto_now_add=True)
	votes = models.IntegerField(default=0)
	is_accepted = models.BooleanField(default=False)
	

