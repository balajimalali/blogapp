from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('sort/<slug:ctg>', views.ctg, name='ctg'),
    path('fetch/<slug:ctg>/<slug:post_slug>', views.post, name='post')
    # path('imageload/', views.loadImg, name='loadImg'),
    # path('imagedel/', views.delImg, name='delImg'),
]