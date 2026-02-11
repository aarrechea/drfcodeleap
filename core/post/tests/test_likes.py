from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from core.post.models import Post, Like

User = get_user_model()

class PostLikeTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', username='testuser', password='password123')
        self.client.force_authenticate(user=self.user)
        self.post = Post.objects.create(user=self.user, title='Test Post', content='Content')
        self.like_url = reverse('post-like', kwargs={'pk': self.post.id})

    def test_like_post(self):
        response = self.client.post(self.like_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['likes_count'], 1)
        self.assertTrue(response.data['is_liked'])
        self.assertTrue(Like.objects.filter(user=self.user, post=self.post).exists())

    def test_unlike_post(self):
        # Like first
        self.client.post(self.like_url)

        # Then unlike
        response = self.client.post(self.like_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['likes_count'], 0)
        self.assertFalse(response.data['is_liked'])
        self.assertFalse(Like.objects.filter(user=self.user, post=self.post).exists())

    def test_unauthenticated_user_cannot_like(self):
        self.client.logout()
        response = self.client.post(self.like_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
