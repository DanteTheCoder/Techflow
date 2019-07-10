from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
from .models import SearchQuery
from posts.models import Post

@login_required
def search_view(request):
	query = request.GET.get('q',None)
	user = None
	if request.user.is_authenticated:
		user = request.user
	if query is not None:
		SearchQuery.objects.create(user=user,query=query)	#This is for saving whatever search made by whom.
		
	qs = (Post.objects.filter(title__icontains=query)|
		Post.objects.filter(content__icontains=query)|
		Post.objects.filter(user__username__icontains=query)|
		Post.objects.filter(tags__name__in=[query]) )

	context = {"object_list" : qs}
	return render(request,'post_list.html',context)