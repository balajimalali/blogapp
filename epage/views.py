from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.views.decorators.http import require_http_methods
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from epage.forms import PostForm
import json
from blogapp.models import Post, Category, Image
from django.utils.text import slugify
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os 

def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""
    def in_groups(u):
        if u.is_authenticated:
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False

    return user_passes_test(in_groups)

# Create your views here.


def gallery(request):
    try:
        msg = request.GET['msg']
    except:
        msg = None
    params = {
        'images': Image.objects.all(),
        'categories': Category.objects.all(),
        'msg': msg
    }
    return render(request, 'epage/gallery.html', params)

@group_required('Administrator')
def categories(request):
    try:
        msg = request.GET['msg']
    except:
        msg = None
    params = {
        'categories': Category.objects.all(),
        'msg': msg
    }
    return render(request, 'epage/category.html', params)
    

@group_required('Author', 'Administrator')
def posts(request):
    params ={
        'posts': Post.objects.filter(author = request.user)
    }
    return render(request, 'epage/posts.html', params)

@group_required('Author', 'Administrator')
def edit_post(request, post_slug):
    if request.method == "POST":
        form = PostForm(request.POST)
        post = Post.objects.get(slug=post_slug)
        if post.author==request.user:
            if form.is_valid():
                post.title = form.cleaned_data['title']
                post.body = form.cleaned_data['body']
                post.desc = form.cleaned_data['desc']
            try:
                if request.POST['status']=='on':
                    post.status = 'published'
            except:
                post.status = 'draft'

            post.category = Category.objects.get(category=request.POST['category'])
            post.save()
            return redirect('/editor/posts') 
        else:
            return redirect('/editor/login')   

    else:
        post = Post.objects.get(slug = post_slug)
        status = False
        if post.status=='published':
            status = True
        params = {
            'form': PostForm(initial={'title':post.title, 'body': post.body, 'desc':post.desc}),
            'categories': Category.objects.all(),
            'is_pub': status,
            'category': post.category.category
        }
        return render(request, 'epage/edit-new.html',params)    

@group_required('Author', 'Administrator')
def newPost(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        post = Post()
        post.author = request.user
        if form.is_valid():
            post.title = form.cleaned_data['title']
            post.body = form.cleaned_data['body']
            post.desc = form.cleaned_data['desc']

        i = 1
        slug = slugify(form.cleaned_data['title'])
        while Post.objects.filter(slug=slug).exists():
            slug = slugify(form.cleaned_data['title']+' #'+str(i))
            i = i+1
        post.slug = slug

        try:
            if request.POST['status']=='on':
                post.status = 'published'
        except:
            post.status = 'draft'
            
        try:
            post.category = Category.objects.get(category=request.POST['category'])
        except:
            post.category = Category.objects.get(category='Default')
        post.save()
        return redirect('/editor/posts') 
    else:
        form = PostForm()
        params = {
            'form': form,
            'categories': Category.objects.all()
        }
        return render(request, 'epage/edit-new.html',params)


@group_required('Author', 'Administrator')
@require_http_methods(['POST'])
def newImg(request):
    request_file = request.FILES['image'] if 'image' in request.FILES else None
    if request_file:
        newImage = Image()

        fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT,'images'), base_url='/media/images')
        stimg = fs.save(request_file.name, request_file)

        # newImage.name = request_file.name
        newImage.name = stimg
        newImage.url = fs.url(stimg)

        try:
            newImage.category = Category.objects.get(category=request.POST['category'])
        except:
            newImage.category = Category.objects.get(category='Default')

        newImage.save()

        return redirect(r'/editor/gallery?msg=image%20added')
    else:
        return redirect(r'/editor/gallery?msg=error%20occured')

@group_required('Author', 'Administrator')
def ehome(request):
    params = {
    }

    return render(request, 'epage/dashboard.html', params)



@group_required('Administrator')
def manageUser(request):
    try:
        msg = request.GET['msg']
    except:
        msg = None

    params = {
        'users': User.objects.filter(is_superuser=False, groups__name='Author'),
        'msg': msg
    }
    return render(request, 'epage/manUser.html', params)

@group_required('Author', 'Administrator')
def preview(request):
    return render(request, 'epage/preview.html')

@group_required('Administrator')
def createUser(request):
    if request.POST.get('password') == request.POST.get('confirmpassword'):
        try:
            user = User.objects.create_user(request.POST.get('username'),request.POST.get('email'),request.POST.get('password'))
            user.save()
            return redirect(r'/editor/users?msg=user%20created')
        except:
            return redirect(r'/editor/users?msg=enter%20credentials%20properly')
    else:
        return redirect(r'/editor/users?msg=enter%20credentials%20properly')

@group_required('Administrator')
def createCategory(request):
    if request.POST.get('category')!='':
        cat = Category()
        cat.category = request.POST.get('category')
        cat.desc = request.POST.get('desc')
        cat.save()
        return redirect(r'/editor/categories?msg=category%20created')
    else:
        return redirect(r'/editor/categories?msg=enter%20details%20properly')


def signin(request):
    if request.user.is_authenticated:
        logout(request)
    if request.method == 'GET':
        try:
            rol = request.GET['next']
            params = {
                "rol": rol
            }
        except:
            params = {}
        return render(request, 'epage/login.html', params)
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(request.POST['redirect'])
        else:
            return render(request, 'epage/login.html', {'error': 'enter correct credentials'})