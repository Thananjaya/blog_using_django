from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from .models import Post
from .forms import SharePostForm, CommentForm

def post_index(request):
	"""
		returns list of published posts

		arguement:
			request: http request
	"""
	post_lists = Post.objects.filter(status="published")
	paginator = Paginator(post_lists, 5)
	page_number = request.GET.get('page')
	try:
		posts = paginator.page(page_number)
	except EmptyPage:
		posts = paginator.page(1)
	except PageNotAnInteger:
		posts = paginator.page(paginator.num_pages)
	return render(request, 'blog/post/index.html', { 'posts': posts })


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
		comment_form = CommentForm(data = request.POST)
		if comment_form.is_valid():
			new_comment = comment_form.save(commit = False)
			new_comment.post = post
			new_comment.save()
	else:
		comment_form = CommentForm()

	return render(request, 'blog/post/detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form, 'new_comment': new_comment })


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
			# cleaned data will be having the form data that is valid
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


#  class based view
class PostIndexView(ListView):
	queryset = Post.objects.filter(status="published")
	context_object_name = 'posts'
	paginate_by  = 2
	template_name = 'blog/post/index.html'

