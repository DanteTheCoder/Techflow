from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class LoginUser(forms.Form):
	username = forms.CharField(label=(""),widget=forms.TextInput(attrs={'class':'form-control','placeholder':'User Name'}))
	password = forms.CharField(label=(""),widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))

class UserCreateForm(UserCreationForm):

	#username = forms.CharField(label=(""),widget=forms.TextInput(attrs={'class':'form-control','placeholder':'User Name'}))
	#password1 = forms.CharField(label=(""),widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))
	#password2 = forms.CharField(label=(""),widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password Confirm'}))
	name = forms.CharField(max_length=30)
	surname = forms.CharField(max_length=30)

	class Meta:
		model = User
		fields=('name','surname','username','password1','password2')

	def __init__(self, *args, **kwargs):
		super(UserCreateForm, self).__init__(*args, **kwargs)

		for fieldname in self.fields:
			self.fields[fieldname].help_text = None	
			self.fields[fieldname].widget.attrs['class'] = 'form-control'
			self.fields[fieldname].label = ''

		self.fields['username'].widget.attrs['placeholder'] = 'User Name'			
		self.fields['password1'].widget.attrs['placeholder'] = 'Password'
		self.fields['password2'].widget.attrs['placeholder'] = 'Password Confirm'
		self.fields['name'].widget.attrs['placeholder'] = 'Your First Name'
		self.fields['surname'].widget.attrs['placeholder'] = 'Your Last Name'

	def save(self, commit=True):
		user = super(UserCreationForm, self).save(commit=False)
		user.set_password(self.cleaned_data["password1"])
		user.first_name = self.cleaned_data['name']
		user.last_name = self.cleaned_data['surname']
		if commit:
			user.save()
		return user