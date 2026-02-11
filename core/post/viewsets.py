from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import CursorPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import Post, Like
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

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user

        like_obj = Like.objects.filter(user=user, post=post).first()

        if like_obj:
            like_obj.delete()
        else:
            Like.objects.create(user=user, post=post, like=True)

        # Refresh from db to get updated counts if needed, or just serialize
        serializer = self.get_serializer(post)
        return Response(serializer.data)

