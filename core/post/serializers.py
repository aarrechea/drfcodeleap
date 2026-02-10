from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'user', 'username', 'created_datetime', 'title', 'content', 'updated_datetime')
        read_only_fields = ('id', 'created_datetime', 'user', 'username', 'updated_datetime')
