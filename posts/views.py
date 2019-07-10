from django.shortcuts import render, get_object_or_404
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

class PostListView(ListView):
	template_name = 'post_list.html'
	queryset = Post.objects.all()
	
class PostDetailView(DetailView):
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
		image = request.POST.get('image')
		user = request.user

		answer = Answer.objects.create(content=content,image=image,user=user,post=post)
		return JsonResponse({'content': content, 'user' : request.user.username, 'timestamp': answer.timestamp})

class PostCreateView(CreateView):
	template_name = 'form.html'
	form_class = PostModelForm
	queryset = Post.objects.all()

class PostUpdateView(UpdateView):
	template_name = './form.html'
	form_class = PostModelForm

	def get_object(self):
		id_ = self.kwargs.get("id")
		return get_object_or_404(Post, id=id_)

class PostDeleteView(DeleteView):

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
	obj = Post.objects.filter(id=id)
	if obj and is_down:
		count = count -1
		obj.update(votes=count)
	elif obj and not is_down:
		count = count +1
		obj.update(votes=count)
	return JsonResponse({'new': count})

def delete_answer(request,id_p,id_a):
	obj = Answer.objects.filter(id=id_a)
	obj.delete()
	url = f"/posts/{id_p}/{id_a}/delete"
	return JsonResponse({"url": url})	