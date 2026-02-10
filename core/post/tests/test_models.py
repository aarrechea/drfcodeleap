from django.test import TestCase
from django.contrib.auth import get_user_model
from core.post.models import Post, Like, Comment

User = get_user_model()

class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', username='testuser', password='password123')

    def test_post_creation(self):
        post = Post.objects.create(
            user=self.user,
            title='Test Post',
            content='This is a test content.'
        )
        self.assertEqual(post.user.email, 'test@example.com')
        self.assertEqual(post.title, 'Test Post')
        self.assertEqual(post.content, 'This is a test content.')
        self.assertIsNotNone(post.created_datetime)

    def test_string_representation(self):
        post = Post(user=self.user, title='Test Post')
        self.assertEqual(str(post), 'test@example.com - Test Post')

    def test_like_creation(self):
        post = Post.objects.create(
            user=self.user,
            title='Test Post',
            content='This is a test content.'
        )
        like = Like.objects.create(
            user=self.user,
            post=post,
            like=True
        )
        self.assertEqual(like.user, self.user)
        self.assertEqual(like.post, post)
        self.assertEqual(like.like, True)

    def test_comment_creation(self):
        post = Post.objects.create(
            user=self.user,
            title='Test Post',
            content='This is a test content.'
        )
        comment = Comment.objects.create(
            user=self.user,
            post=post,
            comment='This is a test comment.'
        )
        self.assertEqual(comment.user, self.user)
        self.assertEqual(comment.post, post)
        self.assertEqual(comment.comment, 'This is a test comment.')
        self.assertIsNotNone(comment.created_datetime)
