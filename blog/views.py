from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from .models import Post
from .forms import PostForm, CommentForm


class PostListView(generic.ListView):
    template_name = 'blog/post_list.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        return Post.objects.filter(status='pup').order_by('-datetime_modified')


# class PostDetailView(LoginRequiredMixin, generic.DetailView):
#     model = Post
#     template_name = 'blog/post_detail.html'
#     context_object_name = 'post'
@login_required
def post_detail_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post_comments = post.comments.all()
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.user = request.user
            new_comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()
    return render(request, 'blog/post_detail.html',{
        'post': post,
        'comments': post_comments,
        'comment_form': comment_form,
    })


class CreatePostView(LoginRequiredMixin, generic.CreateView):
    form_class = PostForm
    template_name = 'blog/create_post.html'
    context_object_name = 'form'


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Post
    template_name = 'blog/create_post.html'
    form_class = PostForm

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Post
    template_name = 'blog/post_delete.html'
    success_url = reverse_lazy('blog')

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user

# def blog_post_list_view(request):
#     post_list = Post.objects.filter(status='pup').order_by('-datetime_modified')
#     return render(request, 'blog/post_list.html', {'post_list': post_list})

# def post_detail_view(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     return render(request, 'blog/post_detail.html', {'post': post})

# def create_post(request):
#     if request.method == 'POST':
#         form = PostForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('blog')
#     else:
#         form = PostForm()
#     return render(request, 'blog/create_post.html', context={'form': form})

# def post_update_view(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     form = PostForm(request.POST or None, instance=post)
#     if form.is_valid():
#         form.save()
#         return redirect(f'/blog/{pk}/')
#     return render(request, 'blog/create_post.html', context={'form': form})

# def post_delete_view(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     if request.method == 'POST':
#         post.delete()
#         return redirect('blog')
#
#     return render(request, 'blog/post_delete.html', {'post': post})
