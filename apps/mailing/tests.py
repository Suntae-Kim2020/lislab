from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import MailingList, EmailCampaign, EmailLog

User = get_user_model()


class MailingListModelTest(TestCase):
    """메일링 리스트 모델 테스트"""

    def setUp(self):
        self.mailing = MailingList.objects.create(
            email='test@example.com'
        )

    def test_mailing_creation(self):
        """메일링 구독 생성 테스트"""
        self.assertEqual(self.mailing.email, 'test@example.com')
        self.assertTrue(self.mailing.is_active)

    def test_unsubscribe_token(self):
        """구독 해지 토큰 생성 테스트"""
        self.assertIsNotNone(self.mailing.unsubscribe_token)


class EmailCampaignModelTest(TestCase):
    """이메일 캠페인 모델 테스트"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='admin',
            password='adminpass123'
        )

        self.campaign = EmailCampaign.objects.create(
            title='Test Campaign',
            subject='Test Subject',
            content_html='<p>Test</p>',
            created_by=self.user
        )

    def test_campaign_creation(self):
        """캠페인 생성 테스트"""
        self.assertEqual(self.campaign.title, 'Test Campaign')
        self.assertEqual(self.campaign.status, EmailCampaign.Status.DRAFT)
