from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LoginView, RegisterView, RefreshView, UserProfileView, MeView, LogoutView

router = DefaultRouter(trailing_slash = False)
router.register('profile', UserProfileView)

urlpatterns = [
    path('me', MeView.as_view()),
    path('', include(router.urls)),
    path('login', LoginView.as_view()),
    path('logout', LogoutView.as_view()),
    path('refresh', RefreshView.as_view()),
    path('register', RegisterView.as_view()),
]