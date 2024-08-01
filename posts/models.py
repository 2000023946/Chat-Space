from django.db import models
from datetime import datetime
from home.models import Post
from django.contrib.auth.models import User

# Create your models here.
class Blog(models.Model):
    post = models.ManyToManyField(Post)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    created_user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    date = models.DateField(default=datetime.now(), blank=True)
    number_users = models.IntegerField(default=0)
    state = models.BooleanField(default=True)
    def __str__(self):
        return f"blog called {self.title} and users:{self.number_users}"
class Request(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, blank=True)
class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    blog = models.ManyToManyField(Blog, related_name="members", blank=True)
    requests = models.ManyToManyField(Request, related_name="ask_members", blank=True)