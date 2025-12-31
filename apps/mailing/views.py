from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .models import MailingList, EmailCampaign, EmailLog
from .serializers import (
    MailingListSerializer,
    MailingSubscribeSerializer,
    EmailCampaignListSerializer,
    EmailCampaignDetailSerializer,
    EmailCampaignCreateUpdateSerializer,
    EmailLogSerializer
)


class MailingListViewSet(viewsets.ModelViewSet):
    """
    메일링 리스트 ViewSet

    - list: 구독자 목록 조회 (관리자만)
    - create: 메일링 구독
    - destroy: 구독 해지
    """

    queryset = MailingList.objects.all()
    serializer_class = MailingListSerializer

    def get_permissions(self):
        if self.action in ['create', 'unsubscribe']:
            return [AllowAny()]
        return [IsAuthenticated()]

    def list(self, request, *args, **kwargs):
        """구독자 목록 조회 (관리자만)"""
        if not request.user.is_admin:
            return Response(
                {"detail": "권한이 없습니다."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """메일링 구독"""
        serializer = MailingSubscribeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"detail": "메일링 리스트에 구독되었습니다."},
            status=status.HTTP_201_CREATED
        )

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def unsubscribe(self, request):
        """메일링 구독 해지 (토큰 사용)"""
        token = request.data.get('token')
        if not token:
            return Response(
                {"detail": "토큰이 필요합니다."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            mailing = MailingList.objects.get(unsubscribe_token=token)
            mailing.is_active = False
            mailing.unsubscribed_at = timezone.now()
            mailing.save()

            return Response(
                {"detail": "메일링 구독이 해지되었습니다."},
                status=status.HTTP_200_OK
            )
        except MailingList.DoesNotExist:
            return Response(
                {"detail": "유효하지 않은 토큰입니다."},
                status=status.HTTP_404_NOT_FOUND
            )


class EmailCampaignViewSet(viewsets.ModelViewSet):
    """
    이메일 캠페인 ViewSet (관리자 전용)

    - list: 캠페인 목록 조회
    - retrieve: 캠페인 상세 조회
    - create: 캠페인 생성
    - update: 캠페인 수정
    - destroy: 캠페인 삭제
    """

    queryset = EmailCampaign.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if not self.request.user.is_admin:
            return EmailCampaign.objects.none()
        return super().get_queryset()

    def get_serializer_class(self):
        if self.action == 'list':
            return EmailCampaignListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return EmailCampaignCreateUpdateSerializer
        return EmailCampaignDetailSerializer

    def perform_create(self, serializer):
        """캠페인 생성 (관리자만)"""
        if not self.request.user.is_admin:
            return Response(
                {"detail": "권한이 없습니다."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def send(self, request, pk=None):
        """캠페인 발송 (관리자만)"""
        if not request.user.is_admin:
            return Response(
                {"detail": "권한이 없습니다."},
                status=status.HTTP_403_FORBIDDEN
            )

        campaign = self.get_object()

        if campaign.status != EmailCampaign.Status.DRAFT:
            return Response(
                {"detail": "임시저장 상태의 캠페인만 발송할 수 있습니다."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 활성 구독자 조회
        subscribers = MailingList.objects.filter(is_active=True)

        # 캠페인 정보 업데이트
        campaign.status = EmailCampaign.Status.SENDING
        campaign.total_recipients = subscribers.count()
        campaign.save()

        # 발송 로그 생성 (실제 발송 로직은 Celery 등 비동기 작업으로 처리)
        for subscriber in subscribers:
            EmailLog.objects.create(
                campaign=campaign,
                recipient=subscriber.email,
                status=EmailLog.Status.PENDING
            )

        # TODO: 실제 이메일 발송 비동기 작업 실행

        return Response(
            {"detail": f"{campaign.total_recipients}명에게 이메일 발송을 시작했습니다."},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def logs(self, request, pk=None):
        """캠페인 발송 로그 조회"""
        if not request.user.is_admin:
            return Response(
                {"detail": "권한이 없습니다."},
                status=status.HTTP_403_FORBIDDEN
            )

        campaign = self.get_object()
        logs = campaign.logs.all()
        serializer = EmailLogSerializer(logs, many=True)
        return Response(serializer.data)
