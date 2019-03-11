from django.shortcuts import render, get_object_or_404
from .models import Post

def post_index(request):
	"""
		returns list of publoshed posts

		arguement:
			request: http request
	"""
	posts = Post.published.all()
	return render(request, 'blog/post/index.html', { 'posts': posts})


def post_show(request, year, month, day, post):
	"""
		returns a detailed information about a partivular post

		arguements:
			request: http request
			year: year parameter, integer, for filtering over the list of posts
			month: month parameter, integer, for filtering over the list of posts
			day: day parameter, integer, for filtering over the list of posts
			post: slug for filtering over the list of posts
	"""
	post = get_object_or_404(Post, slug = post, status='published', publish__year = year, publish__month = month, publish__day = day)
	return render(request, 'blog/post/detail.html', {'post': post})