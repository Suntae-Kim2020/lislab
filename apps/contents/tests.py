import shutil
import tempfile

from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
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


class ContentAdminFileReplaceTest(TestCase):
    """관리자 화면에서 HTML 소스 파일 교체 테스트"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # 업로드 파일이 실제 media/ 에 쌓이지 않도록 임시 디렉터리를 쓴다.
        media_root = tempfile.mkdtemp()
        cls.addClassCleanup(shutil.rmtree, media_root, ignore_errors=True)
        cls._media_override = override_settings(MEDIA_ROOT=media_root)
        cls._media_override.enable()
        cls.addClassCleanup(cls._media_override.disable)

    def setUp(self):
        self.superuser = User.objects.create_superuser(
            username='admin_file_user',
            email='admin-file@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='파일 교체 테스트',
            slug='file-replace-test'
        )
        self.content = Content.objects.create(
            title='교체 대상',
            slug='replace-target',
            content_html='<p>old</p>',
            html_source_file=SimpleUploadedFile('old.html', b'<p>old</p>'),
            category=self.category,
            author=self.superuser,
            status=Content.Status.DRAFT
        )
        self.client.force_login(self.superuser)

    def _post_data(self, **overrides):
        data = {
            'title': self.content.title,
            'summary': '',
            'content_html': self.content.content_html,
            'category': self.category.id,
            'tags': [],
            'difficulty': self.content.difficulty,
            'order': self.content.order,
            'author': self.superuser.id,
            'status': Content.Status.DRAFT,
            'version': self.content.version,
            'estimated_time': 0,
            'prerequisites': '',
            'learning_objectives': '',
            'meta_description': '',
            'meta_keywords': '',
            # ContentVersion 인라인 관리 폼
            'versions-TOTAL_FORMS': '0',
            'versions-INITIAL_FORMS': '0',
            'versions-MIN_NUM_FORMS': '0',
            'versions-MAX_NUM_FORMS': '1000',
        }
        data.update(overrides)
        return data

    def test_clear_checkbox_with_new_file_replaces_content(self):
        """'취소' 체크와 새 파일 선택을 동시에 해도 새 파일로 교체된다"""
        new_file = SimpleUploadedFile('new.html', '<p>새 본문</p>'.encode('utf-8'))
        response = self.client.post(
            f'/admin/contents/content/{self.content.id}/change/',
            self._post_data(
                html_source_file=new_file,
                **{'html_source_file-clear': 'on'}
            )
        )
        self.assertEqual(response.status_code, 302)

        self.content.refresh_from_db()
        self.assertIn('new', self.content.html_source_file.name)
        self.assertEqual(self.content.content_html, '<p>새 본문</p>')

    def test_clear_checkbox_alone_removes_file(self):
        """'취소'만 체크하면 기존 파일이 제거된다"""
        response = self.client.post(
            f'/admin/contents/content/{self.content.id}/change/',
            self._post_data(**{'html_source_file-clear': 'on'})
        )
        self.assertEqual(response.status_code, 302)

        self.content.refresh_from_db()
        self.assertFalse(self.content.html_source_file)

    def test_new_file_alone_replaces_content(self):
        """파일만 선택해도 기존처럼 교체된다"""
        new_file = SimpleUploadedFile('only.html', '<p>파일만</p>'.encode('utf-8'))
        response = self.client.post(
            f'/admin/contents/content/{self.content.id}/change/',
            self._post_data(html_source_file=new_file)
        )
        self.assertEqual(response.status_code, 302)

        self.content.refresh_from_db()
        self.assertIn('only', self.content.html_source_file.name)
        self.assertEqual(self.content.content_html, '<p>파일만</p>')
