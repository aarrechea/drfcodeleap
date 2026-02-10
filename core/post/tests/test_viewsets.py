from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from core.post.models import Post

User = get_user_model()

class PostViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='apiuser@example.com', password='password123')
        self.client.force_authenticate(user=self.user)

        self.post_data = {
            'user': self.user,
            'title': 'API Post',
            'content': 'Content via API'
        }
        self.post = Post.objects.create(**self.post_data)
        self.list_url = reverse('post-list')
        self.detail_url = reverse('post-detail', kwargs={'pk': self.post.id})

    def test_list_posts(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_post(self):
        new_post_data = {
            'title': 'New Post',
            'content': 'New Content'
        }
        response = self.client.post(self.list_url, new_post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)
        self.assertEqual(response.data['title'], 'New Post')
        self.assertEqual(response.data['user'], self.user.id)

    def test_retrieve_post(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'API Post')

    def test_update_post(self):
        update_data = {
            'title': 'Updated Title',
            'content': 'Updated Content'
        }
        response = self.client.put(self.detail_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Title')
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated Title')

    def test_delete_post(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 0)
