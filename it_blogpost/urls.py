from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('blogposts/', views.blogposts, name='blogposts'),
    path('category/<tag>/', views.blogposts, name='category'),

    path('blogpost/create/', views.blogpost_create, name='post-create'),
    path('blogpost/edit/<slug>/', views.blogpost_edit, name='post-edit'),
    path('blogpost/delete/<slug>/', views.blogpost_delete, name='post-delete'),
    path('blogpost/<slug>/', views.blogpost, name='post-detail'),
    path('blogpost/like/<pk>/', views.like_post, name='like-post'),

    path('commentsent/<pk>/', views.comment_sent, name='comment-sent'),
    path('comment/delete/<pk>/', views.comment_delete, name='comment-delete'),
    path('comment/like/<pk>/', views.like_comment, name='like-comment'),

    path('replysent/<pk>/', views.reply_sent, name='reply-sent'),
    path('reply/delete/<pk>/', views.reply_delete, name='reply-delete'),
    path('reply/like/<pk>/', views.like_reply, name='like-reply'),
]
