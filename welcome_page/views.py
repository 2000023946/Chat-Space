from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from posts.models import customuser

# Create your views here.

def index(request):
    return render(request, "welcome_page/index.html",{
    })
def login(request):
    if request.user.is_authenticated:
        return redirect(reverse("home"))
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect(reverse("home"))
        else:
            messages.error(request, "Invalid credentials")
            return redirect(reverse("login"))
    return render(request, "welcome_page/login.html")
def sign_up(request):
    if request.method == "POST":
        if not customuser.objects.filter(id=request.user.id).exists():
            logout(request)
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        password2 = request.POST["password2"]
        if password == password2:
            if customuser.objects.filter(username=username).exists():
                messages.error(request, "Username already exists")
                return redirect((reverse("sign_up")))
            elif customuser.objects.filter(email=email).exists():
                messages.error(request, "Email already exists")
                return redirect(reverse("sign_up"))
            else:
                user = customuser.objects.create_user(username=username, email=email, password=password)
                user.save()
                messages.success(request, "User created successfully!")
                return redirect(reverse("login"))
        else:
            messages.error(request, "Passwords do not match")
            return redirect(reverse("sign_up"))
    else:
        return render(request, "welcome_page/sign_up.html")
