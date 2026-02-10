from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255)
    content = models.TextField(max_length=500)
    likes = models.ManyToManyField(User, related_name='likes', blank=True, through='Like')
    comments = models.ManyToManyField(User, related_name='comments', blank=True, through='Comment')

    def __str__(self):
        return self.user.email + " - " + self.title


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_datetime = models.DateTimeField(auto_now_add=True)
    like = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email + " - " + self.post.title


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_datetime = models.DateTimeField(auto_now_add=True)
    comment = models.CharField(max_length=500)

    def __str__(self):
        return self.user.email + " - " + self.post.title
