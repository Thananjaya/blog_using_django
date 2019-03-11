from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	list_display = ('author', 'title', 'body', 'slug', 'status', 'publish')
	list_filter = ('author', 'status', 'publish', 'created')
	search_fields = ('title', 'body')
	prepopulated_fields = {'slug': ('title',)}
	raw_id_fields = ('author',)
	date_hierarchy = 'publish'
	ordering = ('status', 'publish')