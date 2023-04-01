from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'author', 'status', 'user']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text', )
