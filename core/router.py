from rest_framework import routers
from core.post.viewsets import PostViewSet
from core.authentication.viewsets.register import RegisterViewSet
from core.authentication.viewsets.login import LoginViewSet
from core.authentication.viewsets.refresh import RefreshViewSet

router = routers.DefaultRouter()
router.register(r'post', PostViewSet, basename='post')
router.register(r'auth/register', RegisterViewSet, basename='auth-register')
router.register(r'auth/login', LoginViewSet, basename='auth-login')
router.register(r'auth/refresh', RefreshViewSet, basename='auth-refresh')
