from django.contrib import admin
from .models import Blog, Request, customuser
# Register your models here.

admin.site.register(Blog)
admin.site.register(Request)
admin.site.register(customuser)
