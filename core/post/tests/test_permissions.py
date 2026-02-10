from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from core.post.models import Post

User = get_user_model()


class PostPermissionsTest(APITestCase):
    """
    Test suite for post ownership permissions.
    Ensures only owners can modify/delete their posts while all
    authenticated users can read posts.
    """

    def setUp(self):
        """
        Create two users and a post owned by user1.
        """
        # Create two users
        self.user1 = User.objects.create_user(
            email='user1@example.com',
            username='user1',
            password='password123'
        )

        self.user2 = User.objects.create_user(
            email='user2@example.com',
            username='user2',
            password='password123'
        )

        # Create a post owned by user1
        self.post = Post.objects.create(
            user=self.user1,
            title='User1 Post',
            content='Content by user1'
        )

        self.detail_url = reverse('post-detail', kwargs={'pk': self.post.id})
        self.list_url = reverse('post-list')


    def test_unauthenticated_user_cannot_access_posts(self):
        """
        Test that unauthenticated users cannot access posts.
        """
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_authenticated_user_can_read_all_posts(self):
        """
        Test that any authenticated user can read posts created by others.
        """
        # User2 tries to read user1's post
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'User1 Post')


    def test_owner_can_update_own_post(self):
        """
        Test that a user can update their own post.
        """
        self.client.force_authenticate(user=self.user1)

        update_data = {
            'title': 'Updated Title',
            'content': 'Updated Content'
        }

        response = self.client.put(self.detail_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Title')

        # Verify database was updated
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated Title')


    def test_non_owner_cannot_update_post(self):
        """
        Test that a user cannot update another user's post.
        """
        # User2 tries to update user1's post
        self.client.force_authenticate(user=self.user2)

        update_data = {
            'title': 'Hacked Title',
            'content': 'Hacked Content'
        }

        response = self.client.put(self.detail_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Verify database was NOT updated
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'User1 Post')


    def test_owner_can_patch_own_post(self):
        """
        Test that a user can partially update their own post.
        """
        self.client.force_authenticate(user=self.user1)
        patch_data = {'title': 'Patched Title'}
        response = self.client.patch(self.detail_url, patch_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Patched Title')

        # Verify database was updated
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Patched Title')


    def test_non_owner_cannot_patch_post(self):
        """
        Test that a user cannot partially update another user's post.
        """
        # User2 tries to patch user1's post
        self.client.force_authenticate(user=self.user2)
        patch_data = {'title': 'Hacked Title'}
        response = self.client.patch(self.detail_url, patch_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Verify database was NOT updated
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'User1 Post')


    def test_owner_can_delete_own_post(self):
        """
        Test that a user can delete their own post.
        """
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify post was deleted
        self.assertEqual(Post.objects.filter(id=self.post.id).count(), 0)


    def test_non_owner_cannot_delete_post(self):
        """
        Test that a user cannot delete another user's post.
        """
        # User2 tries to delete user1's post
        self.client.force_authenticate(user=self.user2)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Verify post was NOT deleted
        self.assertEqual(Post.objects.filter(id=self.post.id).count(), 1)


    def test_authenticated_user_can_create_post(self):
        """
        Test that any authenticated user can create their own posts.
        """
        self.client.force_authenticate(user=self.user2)

        post_data = {
            'title': 'User2 Post',
            'content': 'Content by user2'
        }

        response = self.client.post(self.list_url, post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user'], self.user2.id)
        self.assertEqual(Post.objects.count(), 2)
