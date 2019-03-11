"""
	Note:
		we use angle brackets to capture values as a string
		name parameter is used to name the view so that you can refer the urls by name
"""

from django.urls import path
from . import views

app_name = 'blog'

url_paterns = [
	path('', views.post_index, name='post_index'),
	path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_show, name="post_show")
]