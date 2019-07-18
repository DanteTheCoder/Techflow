from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.views.generic import (
	CreateView,
	DetailView,
	ListView,
	UpdateView,
	DeleteView
	)

from .models import Post, Answer, Comment
from .forms import PostModelForm, AnswerModelForm
# Create your views here.

############################################## POSTS(QUESTIONS) ####################################################

class post_list(ListView):
	template_name = 'post_list.html'
	queryset = Post.objects.all()
	
class post_detail(DetailView):
	# queryset = Post.objects.filter(id__gt=1) to limit where detail view looks

	def get_object(self):
		id_ = self.kwargs.get("id")
		return get_object_or_404(Post, id=id_)

	def get(self, request, *args, **kwargs):
		form = AnswerModelForm(request.POST or None, request.FILES or None)
		id_ = self.kwargs.get("id")
		obj = Post.objects.get(id=id_)
		answers = Answer.objects.filter(post=obj)
		return render(request,'post_detail.html',{'object': obj ,'answers' : answers, 'form':form})	

	def post(self, request, *args, **kwargs): #handling answers
		id_ = self.kwargs.get("id")
		post = Post.objects.get(id=id_)
		content = request.POST.get('content')
		answer = Answer.objects.create(content=content,user=request.user,post=post)
		post.total_answers += 1
		post.save()
		return redirect(f'/posts/{id_}') #JsonResponse({'answer': answer, 'user' : request.user.username, 'timestamp': answer.timestamp})

class post_create(CreateView):
	template_name = 'form.html'
	form_class = PostModelForm
	queryset = Post.objects.all()

class post_update(UpdateView):
	
	def get_object(self):
		id_ = self.kwargs.get("id")
		return get_object_or_404(Post, id=id_)

	def post(self, request, *args, **kwargs):
		id_ = self.kwargs.get("id")
		post = Post.objects.filter(id=id_)
		post.update(content=request.POST.get("content"))
		return JsonResponse({})

class post_delete(DeleteView):

	def get_object(self):
		id_ = self.kwargs.get("id")
		return get_object_or_404(Post, id=id_)

	def get(self, request, *args, **kwargs):
		id_ = self.kwargs.get("id")
		post = Post.objects.get(id=id_)
		post.delete()
		return JsonResponse({})

def vote(request,id):
	count = int(request.POST.get("old"))
	is_down = bool(request.POST.get("is_down")=="true")
	is_answer = bool(request.POST.get("is_answer")=="true")

	if is_answer:
		obj = Answer.objects.filter(id=id)
	else:	
		obj = Post.objects.filter(id=id)
	obj[0].voters.add(request.user)
	print(obj[0].voters.all())
	print(request.user)
	if obj and is_down:
		count = count -1
		obj.update(votes=count)
	elif obj and not is_down:
		count = count +1
		obj.update(votes=count)
	return JsonResponse({'new': count})

def delete_answer(request,id_p,id_a):
	post = Post.objects.get(id=id_p)
	post.total_answers -= 1
	post.save()
	obj = Answer.objects.filter(id=id_a)
	obj.delete()
	url = f"/posts/{id_p}/{id_a}/delete"
	return JsonResponse({"url": url})

def update_answer(request,id_p,id_a):
	obj = Answer.objects.filter(id=id_a)
	obj.update(content=request.POST.get("content"))
	return JsonResponse({})