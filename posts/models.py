from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField
User = settings.AUTH_USER_MODEL


# Create your models here.

class Post(models.Model):
	user = models.ForeignKey(User,default=1,null=True,on_delete=models.SET_NULL,related_name="Post_User")
	title = models.CharField(max_length=90,null=True)
	content = RichTextUploadingField(null=True,blank=False)
	timestamp = models.DateTimeField(auto_now=False,auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	votes = models.IntegerField(default=0)
	total_answers = models.IntegerField(default=0)
	tags = TaggableManager(blank=True)
	voters = models.ManyToManyField(User,blank=True)

	class Meta:
		ordering = ['-updated','-timestamp']

	def get_absolute_url(self):
		return reverse("post:post-detail", kwargs={"id": self.id})

	def __str__(self):
		return '%s' % (self.title)

class Answer(models.Model):
	post = models.ForeignKey(Post,null=True,on_delete=models.SET_NULL)
	user = models.ForeignKey(User,default=1,null=True,on_delete=models.SET_NULL,related_name="Answer_User")
	content = RichTextUploadingField(null=True,blank=False)
	timestamp = models.DateTimeField(auto_now=False,auto_now_add=True)
	votes = models.IntegerField(default=0)
	voters = models.ManyToManyField(User,blank=True)
	is_accepted = models.BooleanField(default=False)

class Comment(models.Model):
	post = models.ForeignKey(Post,null=True,on_delete=models.SET_NULL)
	answer = models.ForeignKey(Answer,null=True,on_delete=models.SET_NULL)
	user = models.ForeignKey(User,default=1,null=True,on_delete=models.SET_NULL,related_name="Comment_User")
	content = RichTextUploadingField(null=True,blank=False)
	timestamp = models.DateTimeField(auto_now=False,auto_now_add=True)
	votes = models.IntegerField(default=0)
	voters = models.ManyToManyField(User,blank=True)
	is_accepted = models.BooleanField(default=False)
