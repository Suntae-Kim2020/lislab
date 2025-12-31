from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.contents.models import Category, Content
from .models import Comment

User = get_user_model()


class CommentModelTest(TestCase):
    """댓글 모델 테스트"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )

        self.content = Content.objects.create(
            title='Test Content',
            slug='test-content',
            summary='Test summary',
            content_html='<p>Test</p>',
            category=self.category,
            author=self.user
        )

        self.comment = Comment.objects.create(
            content=self.content,
            author=self.user,
            text='Test comment'
        )

    def test_comment_creation(self):
        """댓글 생성 테스트"""
        self.assertEqual(self.comment.text, 'Test comment')
        self.assertEqual(self.comment.author, self.user)
        self.assertEqual(self.comment.content, self.content)

    def test_reply_creation(self):
        """답글 생성 테스트"""
        reply = Comment.objects.create(
            content=self.content,
            author=self.user,
            parent=self.comment,
            text='Test reply'
        )
        self.assertEqual(reply.parent, self.comment)
        self.assertEqual(self.comment.replies_count, 1)
