from django import forms
from .models import Post, Answer

class PostModelForm(forms.ModelForm):
	class Meta:
		model = Post
		fields=[
			'title',
			'image',
			'content',
			'tags',
			]

	def __init__(self, *args, **kwargs):
		super(PostModelForm, self).__init__(*args, **kwargs)

		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({
				'class': 'form-control'	
        })
			self.fields[field].label = ''

		self.fields['title'].widget.attrs['placeholder'] = 'Title'
		self.fields['content'].widget.attrs['placeholder'] = 'Content'
		self.fields['tags'].widget.attrs['placeholder'] = 'star,its,css'

class AnswerModelForm(forms.ModelForm):
	class Meta:
		model = Answer
		fields = ['content','image']

	def __init__(self, *args, **kwargs):
		super(AnswerModelForm, self).__init__(*args, **kwargs)

		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({
				'class': 'form-control'	
        })
			self.fields[field].label = ''	

		self.fields['content'].widget.attrs['placeholder'] = 'Content'	