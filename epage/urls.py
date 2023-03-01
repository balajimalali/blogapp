from django.urls import path
from . import views

urlpatterns = [
    path('', views.ehome, name='ehome'),
    path('login/', views.signin, name='signin'),
    # path('preview', views.preview, name='preview'),
    path('posts', views.posts, name='posts'),
    path('post/<slug:post_slug>', views.edit_post, name='edit_posts'),
    path('users', views.manageUser, name='manageUser'),
    path('new', views.newPost, name='newPost'),
    path('new-image', views.newImg, name='newImg'),
    path('categories', views.categories, name='categories'),
    path('gallery', views.gallery, name='gallery'),
    path('create', views.createUser, name='createUser'),
    path('create-category', views.createCategory, name='createCategory'),
]