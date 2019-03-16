from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown
from ..models import Post

register = template.Library()

@register.simple_tag
def total_post_count():
	total_post_count = Post.objects.filter(status = 'published').count()
	return total_post_count


@register.inclusion_tag('blog/post/latest_posts.html')
def latest_posts(count = 4):
	latest_posts = Post.objects.filter(status = 'published').order_by('-publish')[:count]
	return { 'latest_posts': latest_posts }

@register.inclusion_tag('blog/post/most_commented_posts.html')
def most_commented_posts(count = 4):
	most_commented_posts = Post.objects.filter(status = 'published').annotate(total_comments = Count('comments')).order_by('-total_comments')[:count]
	return { 'most_commented_posts': most_commented_posts }

@register.filter(name = 'markdown')
def markdown_format(text):
	return mark_safe(markdown.markdown(text))