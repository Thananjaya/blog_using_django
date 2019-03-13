"""
	Django comes with two base classes to build forms:

		Form: allows us to build standard forms
		ModelForm: allows us to build forms dynamically along with the model
"""
from django import forms
from .models import Comment

class SharePostForm(forms.Form):
	name = forms.CharField(max_length = 25)
	email = forms.EmailField()
	to = forms.EmailField()
	comments = forms.CharField(required = False, widget = forms.Textarea)


class CommentForm(forms.ModelForm):
	class Meta:
		model  = Comment
		fields = ('author', 'email', 'message')
	