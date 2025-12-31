from rest_framework import serializers
from .models import MailingList, EmailCampaign, EmailLog


class MailingListSerializer(serializers.ModelSerializer):
    """메일링 리스트 Serializer"""

    class Meta:
        model = MailingList
        fields = ['id', 'email', 'is_active', 'subscribed_at']
        read_only_fields = ['subscribed_at']


class MailingSubscribeSerializer(serializers.Serializer):
    """메일링 구독 Serializer"""

    email = serializers.EmailField()

    def create(self, validated_data):
        email = validated_data['email']
        mailing, created = MailingList.objects.get_or_create(
            email=email,
            defaults={'is_active': True}
        )

        if not created and not mailing.is_active:
            mailing.is_active = True
            mailing.unsubscribed_at = None
            mailing.save()

        return mailing


class EmailCampaignListSerializer(serializers.ModelSerializer):
    """이메일 캠페인 목록용 Serializer"""

    created_by_name = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = EmailCampaign
        fields = [
            'id', 'title', 'subject', 'status',
            'total_recipients', 'sent_count', 'failed_count',
            'scheduled_at', 'sent_at', 'created_by', 'created_by_name', 'created_at'
        ]


class EmailCampaignDetailSerializer(serializers.ModelSerializer):
    """이메일 캠페인 상세용 Serializer"""

    created_by_name = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = EmailCampaign
        fields = [
            'id', 'title', 'subject', 'content_html', 'content_text',
            'status', 'total_recipients', 'sent_count', 'failed_count',
            'scheduled_at', 'sent_at', 'created_by', 'created_by_name',
            'created_at', 'updated_at'
        ]


class EmailCampaignCreateUpdateSerializer(serializers.ModelSerializer):
    """이메일 캠페인 생성/수정용 Serializer"""

    class Meta:
        model = EmailCampaign
        fields = ['title', 'subject', 'content_html', 'content_text', 'scheduled_at']


class EmailLogSerializer(serializers.ModelSerializer):
    """이메일 발송 로그 Serializer"""

    campaign_title = serializers.CharField(source='campaign.title', read_only=True)

    class Meta:
        model = EmailLog
        fields = [
            'id', 'campaign', 'campaign_title', 'recipient', 'status',
            'error_message', 'sent_at', 'opened_at', 'clicked_at', 'created_at'
        ]
        read_only_fields = ['created_at']
