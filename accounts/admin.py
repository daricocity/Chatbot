from django.contrib import admin
from .models import CustomUser, Jwt, Favorite, UserProfile

# Register your models here.
admin.site.register((CustomUser, Jwt, Favorite, UserProfile))
