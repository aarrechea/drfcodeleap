from rest_framework import viewsets, permissions
from rest_framework.pagination import CursorPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import Post
from .serializers import PostSerializer
from .filters import PostFilter
from core.authentication.permissions import UserPermission


class PostCursorPagination(CursorPagination):
    page_size = 3
    ordering = '-updated_datetime'


class PostViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    queryset = Post.objects.all().order_by('-updated_datetime')
    serializer_class = PostSerializer
    permission_classes = [UserPermission]
    pagination_class = PostCursorPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = PostFilter

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

