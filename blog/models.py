from django.db import models
from django.shortcuts import reverse
from django.contrib.auth import get_user_model


class Post(models.Model):
    STATUS_CHOICES=(
        ('pup', 'Published'),
        ('drf', 'Draft'),
    )
    title = models.CharField(max_length=100)
    text = models.TextField()
    author = models.ForeignKey('auth.User',on_delete=models.CASCADE)
    datetime_create = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=3)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='users',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', args=[self.id])
