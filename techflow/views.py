from django.contrib.auth import authenticate,login,logout
from django.views.generic import DetailView, View
from django.shortcuts import render,redirect
from .forms import LoginUser, UserCreateForm

class home(View):
	def get(self, request, *args, **kwargs):	
		form = LoginUser(request.POST or None)
		template_name = 'home.html'
		return render(request,template_name,{'form': form})	

	def post(self, request, *args, **kwargs):
		print(request.POST)
		if not request.user.is_authenticated:
			username=request.POST.get('username')
			password=request.POST.get('password')
			user = authenticate(username=username,password=password)
			login(request,user)
			return render(request,'home.html')

			return render(request,'form.html',{'form': form})
		else:
			return redirect('/posts/')

class signup(View):
	def get(self, request, *args, **kwargs):	
		form = UserCreateForm(request.POST or None)
		return render(request,'form.html',{'form': form})	

	def post(self,request,*args,**kwargs):
		if not request.user.is_authenticated:
			form = UserCreateForm(request.POST or None)
			if request.method == 'POST':
				if form.is_valid():
					form.save()
					username=form.cleaned_data.get('username')
					raw_password = form.cleaned_data.get('password1')
					user = authenticate(username=username,password=raw_password)
					login(request,user)
					return render(request,'home.html')

			return render(request,'form.html',{'form':form})
		else:
			return redirect('/posts/')
