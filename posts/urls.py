from django.urls import path
from .views import (
	PostListView,
	PostDetailView,
	PostCreateView,
	PostUpdateView,
	PostDeleteView,
	vote,
	delete_answer,
	)

app_name = 'post'
urlpatterns = [
	path('',PostListView.as_view(),name='post-list'),
	path('create/',PostCreateView.as_view()),
	path('<int:id>/',PostDetailView.as_view(), name='post-detail'),
	path('<int:id>/update/',PostUpdateView.as_view()),
	path('<int:id>/delete/',PostDeleteView.as_view()),
	path('<int:id>/vote',vote),
	path('<int:id_p>/<int:id_a>/delete',delete_answer),
]