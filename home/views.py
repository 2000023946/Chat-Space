from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from posts.models import Blog, Request, customuser
from .models import Post
from datetime import datetime
from django.contrib.auth import logout
from welcome_page.models import Recent
from django.db.models import Q
from django.contrib import messages
# Create your views here.

def popularSort(list):
    if len(list) == 0:
        return []
    return_list = [list[0]]
    for blog in list[1:]:
        if return_list[-1].number_users >= blog.number_users and len(return_list) < 5:
            return_list.append(blog)
        elif return_list[-1].number_users < blog.number_users:
            return_list.append(blog)
            cur_index = -1
            while len(return_list) >= (cur_index-1)*-1 and return_list[cur_index-1].number_users < blog.number_users:
                return_list[cur_index] = return_list[cur_index-1]
                return_list[cur_index-1] = blog
                cur_index-=1
        if len(return_list) > 5:
            return_list.pop()
    return return_list

def index(request):
    user_blogs = []
    recents = []
    q_set = None
    if not customuser.objects.filter(id=request.user.id).exists():
        return redirect(reverse("sign_up"))
    elif not request.user.is_authenticated:
        return redirect(reverse("login"))
    if request.user.is_authenticated:
        if 'q' in request.GET:
            q = request.GET['q']
            multiple_q = Q(Q(title__icontains=q) | Q(description__icontains=q))
            q_set = Blog.objects.filter(multiple_q)
        for blog in Blog.objects.all():
            if blog.created_user == request.user:
                user_blogs.append(blog)
        for instance in Recent.objects.filter(user_for=request.user).all():
            if instance.recent_blog not in recents:
                recents.append(instance.recent_blog)
        popular = popularSort(Blog.objects.all())
        print(popular)
        return render(request, "home/index.html", {
            "user" : request.user,
            "blogs" : Blog.objects.all(),
            "user_blogs": user_blogs,
            "recent_blogs": recents[len(recents)-3:len(recents)],
            "popular_blogs":popular,
            "q_set": q_set
        })

def blog_content(request, pk):
    if not request.user.is_authenticated:
        return redirect(reverse("login"))
    blog = Blog.objects.get(id = pk)
    if not blog.state:
        print(blog.state)
        if not customuser.objects.filter(user= request.user, blog=blog).exists():
            messages.error(request, "Can not join Private. Need permissions from creater")
            cur_member = request.user
            creator = blog.created_user
            permission = Request.objects.create(user_from=cur_member, blog=blog, user_to=creator)
            permission.save()
            creator = customuser.objects.get(user=creator)
            creator.requests.add(request)
            creator.save()
            return render(request, "home/index.html",{
                "permissions": customuser.objects.all()
            })
    if request.method == "POST":
        txt_message = request.POST["message"]
        username = request.user.username
        post = Post.objects.create(username=username, txt_message=txt_message)
        post.save()
        blog.post.add(post)
        blog.save()
        cur_member = customuser.objects.get(user=request.user)
        cur_member.blog.add(blog)
        cur_member.save()
        if not Recent.objects.filter(recent_blog=blog, user_for=request.user).exists():
            prev_users = blog.number_users
            blog.number_users = prev_users + 1
            blog.save()
        if Recent.objects.filter(recent_blog=blog, user_for=request.user).exists():
            for recent in Recent.objects.filter(recent_blog=blog, user_for=request.user):
                recent.delete()
                recent.save()
        history = Recent.objects.create(recent_blog=blog, user_for=request.user)
    posts = blog.post.all()
    return render(request, "home/blog_content.html", {
        "posts" : posts,
        "blog" : blog,
        "username": request.user.username
    })
def remove(request, pk, sk):
    blog = Blog.objects.get(id=pk)
    post = blog.post.get(id=sk)
    if request.method == "POST":
        cur_posts = blog.post.all()
        for post in cur_posts:
            if post.id == sk:
                post.delete()
        return redirect(reverse("blog_content", args=(blog.id,)))
    return render(request, "home/remove.html",{
        "blog":blog,
        "post":post
    })
def update(request, pk, sk):
    blog = Blog.objects.get(id=pk)
    post = blog.post.get(id=sk)
    if request.method == "POST":
        new_txt = request.POST["new-txt"]
        post.txt_message = new_txt
        post.save()
        return redirect(reverse("blog_content", args=(blog.id,)))
    return render(request, "home/update.html",{
        "blog":blog,
        "post":post
    })
def logout_user(request):
    logout(request)
    return redirect(reverse("login"))