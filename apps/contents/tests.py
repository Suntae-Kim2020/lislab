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


class ContentSearchVisibilityTest(TestCase):
    """비공개 콘텐츠 검색 노출 테스트"""

    def setUp(self):
        self.admin = User.objects.create_user(
            username='admin_user',
            password='testpass123',
            role=User.Role.ADMIN
        )

        self.category = Category.objects.create(
            name='검색 테스트',
            slug='search-test'
        )

        self.tag = Tag.objects.create(name='비공개태그', slug='private-tag')

        self.public_content = Content.objects.create(
            title='공개 문서',
            slug='public-doc',
            summary='공개 요약',
            content_html='<p>public</p>',
            category=self.category,
            author=self.admin,
            status=Content.Status.PUBLISHED
        )

        self.private_content = Content.objects.create(
            title='비공개 문서',
            slug='private-doc',
            summary='비공개 요약',
            content_html='<p>private</p>',
            category=self.category,
            author=self.admin,
            status=Content.Status.PRIVATE
        )
        self.private_content.tags.add(self.tag)

    def _slugs(self, response):
        return [item['slug'] for item in response.json()['results']]

    def test_private_content_hidden_from_anonymous_search(self):
        """비회원 검색에 비공개 콘텐츠가 나오지 않는다"""
        response = self.client.get('/api/contents/contents/', {'search': '문서'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self._slugs(response), ['public-doc'])

    def test_private_content_hidden_from_admin_search(self):
        """관리자 검색에도 비공개 콘텐츠가 나오지 않는다"""
        self.client.force_login(self.admin)
        response = self.client.get('/api/contents/contents/', {'search': '문서'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self._slugs(response), ['public-doc'])

    def test_private_content_hidden_from_tag_search(self):
        """태그 검색에도 비공개 콘텐츠가 나오지 않는다"""
        self.client.force_login(self.admin)
        response = self.client.get('/api/contents/contents/', {'tag': '비공개태그'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self._slugs(response), [])

    def test_private_content_hidden_from_admin_list(self):
        """관리자가 목록을 조회해도 비공개 콘텐츠는 보이지 않는다"""
        self.client.force_login(self.admin)
        response = self.client.get('/api/contents/contents/')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('private-doc', self._slugs(response))

    def test_private_content_detail_blocked_for_admin(self):
        """관리자가 URL로 직접 들어가도 비공개 콘텐츠 상세는 열리지 않는다"""
        self.client.force_login(self.admin)
        response = self.client.get('/api/contents/contents/private-doc/')
        self.assertEqual(response.status_code, 404)

    def test_private_content_detail_blocked_for_anonymous(self):
        """비회원은 비공개 콘텐츠 상세에 접근할 수 없다"""
        response = self.client.get('/api/contents/contents/private-doc/')
        self.assertIn(response.status_code, (401, 403, 404))

    def test_private_content_visible_in_django_admin(self):
        """Django 관리자 화면에서는 비공개 콘텐츠가 그대로 보인다"""
        superuser = User.objects.create_superuser(
            username='super_user',
            email='super@example.com',
            password='testpass123'
        )
        self.client.force_login(superuser)
        response = self.client.get('/admin/contents/content/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '비공개 문서')

    def test_private_content_hidden_from_favorites(self):
        """즐겨찾기 이후 비공개로 바뀐 콘텐츠는 즐겨찾기 목록에 나오지 않는다"""
        member = User.objects.create_user(
            username='member_user',
            password='testpass123'
        )
        Favorite.objects.create(user=member, content=self.public_content)
        Favorite.objects.create(user=member, content=self.private_content)

        self.client.force_login(member)
        response = self.client.get('/api/contents/favorites/')
        self.assertEqual(response.status_code, 200)
        slugs = [item['content']['slug'] for item in response.json()['results']]
        self.assertEqual(slugs, ['public-doc'])
