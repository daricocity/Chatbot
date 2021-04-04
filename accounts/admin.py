from django.contrib import admin
from .models import CustomUser, Jwt, Favourite

# Register your models here.
admin.site.register((CustomUser, Jwt, Favourite))
