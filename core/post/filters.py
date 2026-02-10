import django_filters
from .models import Post


class PostFilter(django_filters.FilterSet):
    """
    FilterSet for Post model to filter posts by username.

    Usage:
    - Filter by exact username: ?user__username=johndoe
    - Filter by partial username (case-insensitive): ?user__username__icontains=john
    """

    class Meta:
        model = Post
        fields = {
            'user__username': ['exact', 'icontains'],
        }
