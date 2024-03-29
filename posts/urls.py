#  POSTS URLS.PY

from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.PostList.as_view(), name='all'),
    path('new/', views.CreatePost.as_view(), name='create'),
    path('by/<username>/', views.UserPosts.as_view(), name='for_user'),
    path('by/<username>/<int:pk>/', views.PostDetail.as_view(), name='single'),
    path('delete/<int:pk>/', views.DeletePost.as_view(), name='delete'),
    path('edit/<username>/<int:pk>/', views.EditPost.as_view(), name='edit'),

    path('comment/<int:post_pk>/',
         views.CreateComment.as_view(), name='add_comment'),
    path('comment/delete/<int:comment_pk>/',
         views.delete_comment, name='delete_comment'),
]
