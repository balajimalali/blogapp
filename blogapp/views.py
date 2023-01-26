from django.shortcuts import render, HttpResponse, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import Post, Image, Category, Carousel
import json
# import datetime
from django.utils import timezone

# from froala_editor.views import storage

# Create your views here.

def home(request):
    posts = Post.objects.filter(status='published')
    carousel = Carousel.objects.filter(exp__gte=timezone.now())
    # carousel = Carousel.objects.filter(exp__gte=datetime.datetime.now())
    categories = Category.objects.all().exclude(category='Default')
    return render(request, 'blogapp/home.html', {'posts': posts, 'categories': categories, 'carousel':carousel})


def ctg(request, ctg):

    posts = Post.objects.filter(status='published', category= get_object_or_404(Category ,category=ctg))
    categories = Category.objects.all().exclude(category='Default')

    params = {
        'ctg': ctg,
        'posts': posts,
        'categories': categories
    }

    return render(request, 'blogapp/posts.html', params)


def post(request, ctg, post_slug):
    post = get_object_or_404(Post,slug=post_slug,status='published')
    categories = Category.objects.all().exclude(category='Default')

    params = {
        'ctg': ctg,
        'post': post,
        'categories': categories
    }

    return render(request, 'blogapp/post-page.html', params)


# def loadImg(request):

#     imgList = []
#     images = Image.objects.all()
#     for image in images:
#         imgList.append({
#             "url": image.url,
#             "thumb": image.url,
#             "tag": image.name
#         })
#     res = json.dumps(imgList)
#     return HttpResponse(res, content_type="application/json")


# @csrf_exempt
# def delImg(request):
#     try:
#         storage.delete(request.POST['src'].split('/media/')[1])
#         img = Image.objects.filter(url=request.POST['src']).delete()
#         return HttpResponse({'status': 'deleted'}, content_type="application/json")
#     except:
#         return HttpResponse(json.dumps({'error': 'unable to delete'}), content_type="application/json")
        