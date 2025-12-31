from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Category, Tag, Content, Favorite

User = get_user_model()


class ContentModelTest(TestCase):
    """콘텐츠 모델 테스트"""

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
            content_html='<p>Test content</p>',
            category=self.category,
            author=self.user,
            status=Content.Status.PUBLISHED
        )

    def test_content_creation(self):
        """콘텐츠 생성 테스트"""
        self.assertEqual(self.content.title, 'Test Content')
        self.assertEqual(self.content.slug, 'test-content')
        self.assertEqual(self.content.status, Content.Status.PUBLISHED)

    def test_favorite_creation(self):
        """즐겨찾기 생성 테스트"""
        favorite = Favorite.objects.create(
            user=self.user,
            content=self.content
        )
        self.assertEqual(favorite.user, self.user)
        self.assertEqual(favorite.content, self.content)

    def test_content_view_count(self):
        """조회수 증가 테스트"""
        initial_count = self.content.view_count
        self.content.view_count += 1
        self.content.save()
        self.assertEqual(self.content.view_count, initial_count + 1)
