from django.urls import path

from . import views

urlpatterns = [
    path("", views.create_blog, name = "create_blog")
]