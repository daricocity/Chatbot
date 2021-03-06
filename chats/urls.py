from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GenericFileUploadView, MessageView, ReadMultipleMessages

router = DefaultRouter(trailing_slash = False)
router.register('message', MessageView)
router.register("file-upload", GenericFileUploadView)

urlpatterns = [
    path("", include(router.urls)),
    path("read-messages", ReadMultipleMessages.as_view()),
]