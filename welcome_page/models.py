from django.db import models
from django.contrib.auth.models import User
from posts.models import Blog
from datetime import datetime
from posts.models import customuser

# Create your models here.
class Recent(models.Model):
    recent_blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="blog")
    date = models.DateField(default=datetime.today())
    user_for = models.ForeignKey(customuser, on_delete=models.CASCADE, related_name="recents")

