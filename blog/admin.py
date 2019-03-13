from django.contrib import admin
from .models import Post, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	list_display = ('author', 'title', 'body', 'slug', 'status', 'publish')
	list_filter = ('author', 'status', 'publish', 'created')
	search_fields = ('title', 'body')
	prepopulated_fields = {'slug': ('title',)}
	raw_id_fields = ('author',)
	date_hierarchy = 'publish'
	ordering = ('status', 'publish')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	list_display = ('post', 'author', 'message', 'email', 'active')
	list_filter = ('active', 'updated', 'created')
	search_fields = ('author', 'email', 'message')
	raw_id_fields = ('post',)