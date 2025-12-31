from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserModelTest(TestCase):
    """사용자 모델 테스트"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            user_type=User.UserType.STUDENT
        )

    def test_user_creation(self):
        """사용자 생성 테스트"""
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertTrue(self.user.check_password('testpass123'))

    def test_user_role_default(self):
        """기본 역할이 USER인지 확인"""
        self.assertEqual(self.user.role, User.Role.USER)

    def test_is_admin_property(self):
        """관리자 권한 체크"""
        self.assertFalse(self.user.is_admin)

        admin_user = User.objects.create_user(
            username='admin',
            password='adminpass123',
            role=User.Role.ADMIN
        )
        self.assertTrue(admin_user.is_admin)

    def test_can_comment_property(self):
        """댓글 작성 권한 체크"""
        self.assertTrue(self.user.can_comment)

        guest = User(role=User.Role.GUEST)
        self.assertFalse(guest.can_comment)
