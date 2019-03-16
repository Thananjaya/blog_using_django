"""
	Sitemap is an xml file that interacts with the search engines.
	Sitemap tells search-engine indexers how frequently your pages change 
	and how “important” certain pages are in relation to other pages on your site. 
	This information helps search engines index your site.
	Sitemap class represents a "section" of entries in your sitemap
"""
from django.contrib.sitemaps import Sitemap
from .models import Post


def PostSitemap(Sitemap):
	"""
		Variables:
			changefreq and priority attributes indicates the change frequency of your post pages,
			the maximum value is 1
		Functions:
			items() is simply a method that returns a list of objects.
			lastmod(), will receives the each object returned by items() and returns the last updated time of the object, should return a datetime.
	"""
	changefreq = 'weekly'
	priority = 0.9


	def items():
		return Post.objects.filter(status = 'published').all()


	def lastmod(self, obj):
		return obj.updated
