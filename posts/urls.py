from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import (
	post_list,
	post_detail,
	post_create,
	post_update,
	post_delete,
	vote,
	delete_answer,
	update_answer,
	)

app_name = 'post'
urlpatterns = [
	path('',login_required(post_list.as_view()),name='post-list'),
	path('create/',post_create.as_view()),
	path('<int:id>/',post_detail.as_view(), name='post-detail'),
	path('<int:id>/update/',post_update.as_view()),
	path('<int:id>/delete/',post_delete.as_view()),
	path('<int:id>/vote',vote),
	path('<int:id_p>/<int:id_a>/delete',delete_answer),
	path('<int:id_p>/<int:id_a>/update',update_answer),	
]