from django.contrib import admin
from .models import Message, MessageAttachment, GenericFileUpload

# Register your models here.
admin.site.register((Message, MessageAttachment, GenericFileUpload))
