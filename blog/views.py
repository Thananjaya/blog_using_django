from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from django.db.models import Count
from django.contrib.postgres.search import SearchVector
from .models import Post
from .forms import SharePostForm, CommentForm, SearchForm
from taggit.models import Tag

def post_index(request, tag_slug=None):
	"""
		returns list of published posts

		arguement:
			request: http request
			tag_slug: required by the taggit model
	"""
	post_lists = Post.objects.filter(status = "published")
	tag = None
	if tag_slug:
		tag = get_object_or_404(Tag, slug = tag_slug)
		post_lists = Post.objects.filter(tags__in = [tag])
	paginator = Paginator(post_lists, 5)
	page_number = request.GET.get('page')
	try:
		posts = paginator.page(page_number)
	except EmptyPage:
		posts = paginator.page(1)
	except PageNotAnInteger:
		posts = paginator.page(paginator.num_pages)
	return render(request, 'blog/post/index.html', { 'posts': posts, 'tag': tag })


def post_show(request, year, month, day, post):
	"""
		returns a detailed information about a particular post

		arguements:
			request: http request
			year: year parameter, integer, for filtering over the list of posts
			month: month parameter, integer, for filtering over the list of posts
			day: day parameter, integer, for filtering over the list of posts
			post: slug for filtering over the list of posts
	"""
	post = get_object_or_404(Post, slug = post, status='published', publish__year = year, publish__month = month, publish__day = day)
	comments = post.comments.filter(active = True)
	new_comment = None

	if request.method == 'POST':
		comment_form_data = CommentForm(request.POST)
		if comment_form_data.is_valid():
			new_comment = comment_form_data.save(commit = False)
			new_comment.post = post
			new_comment.save()
	else:
		comment_form = CommentForm()

	post_tags_id = post.tags.values_list('id', flat = True)
	similar_posts = Post.objects.filter(status = 'published', tags__in = post_tags_id).exclude(id = post.id)
	return render(request, 'blog/post/detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form, 'new_comment': new_comment, 'similar_posts':similar_posts })


def share_post(request, post_id):
	"""
		Sharing a post via email,

		Arguements:
			request: HTTP request
			post_id: id of the post
	"""
	post = get_object_or_404(Post, id = post_id, status = "published")
	sent = False
	if request.method == 'POST':
		form =  SharePostForm(request.POST)
		if form.is_valid():
			# cleaned data will be having the valid data that is been entered in the form
			valid_data = form.cleaned_data
			# used to difne the url for the user to click, since post detail page is defined by slug rule
			post_url = request.build_absolute_uri(post.get_absolute_url())
			subject = "{} asks you to read {}".format(valid_data['name'], post.title)
			message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, valid_data['name'], valid_data['comments'])
			send_mail(subject, message, 'thananthanan@gmail.com', [valid_data['to']])
			sent = True
	else:
		form = SharePostForm()
	return render(request, 'blog/post/share_post_form.html', { 'post': post, 'form': form, 'sent': sent })


def search_post(request):
	form = SearchForm()
	query = None
	results = []
	if 'search_query' in request.GET:
		form = SearchForm(request.GET)
		if form.is_valid():
			query = form.cleaned_data['search_query']
			results = Post.objects.annotate(search = SearchVector('title', 'body')).filter(search = query)
	return render(request, 'blog/post/search_post.html', {'form': form, 'results': results, 'query': query})

#  class based view
class PostIndexView(ListView):
	queryset = Post.objects.filter(status="published")
	context_object_name = 'posts'
	paginate_by  = 2
	template_name = 'blog/post/index.html'

