"""
	Note:
		we use angle brackets to capture values as a string
		name parameter is used to name the view so that you can refer the urls by name
"""

from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
	path('', views.post_index, name="post_index"),
	path('tag/<slug:tag_slug>', views.post_index, name="post_index_filtered_by_tag"),
	# path('', views.PostIndexView.as_view(), name='post_index_class'),
	path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_show, name="post_show"),
	path('<int:post_id>/share/', views.share_post, name="share_post")
]