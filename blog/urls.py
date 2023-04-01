from django.urls import path
from . import views


urlpatterns = [
    path('', views.PostListView.as_view(), name='blog'),
    path('<int:pk>/', views.post_detail_view, name='post_detail'),
    path('create/', views.CreatePostView.as_view(), name='create_post'),
    path('<int:pk>/update/', views.PostUpdateView.as_view(), name='post_update'),
    path('<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete')

]
