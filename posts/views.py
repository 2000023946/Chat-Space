from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Blog, Request, customuser
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.

def create_blog(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        state = request.POST["state"]
        state = state.lower()
        if state == "public" or state == "private" or len(state) == 0:
            created_user = request.user
            if state == "public" or len(state) == 0:
                blog = Blog.objects.create(title=title, description=description, created_user=created_user, state=True)
            else:
                blog = Blog.objects.create(title=title, description=description, created_user=created_user, state=False)
            cur_member = customuser.objects.get(user=request.customuser)
            cur_member.blog.add(blog)
            cur_member.save()
            blog.save()
            return redirect(reverse("home"))
        else:
            messages.error(request, "Enter public or private or leave blank for public ")
            return redirect(reverse("create_blog"))
    return render(request, "posts/create_blog.html")
