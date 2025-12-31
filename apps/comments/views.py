from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Comment
from .serializers import CommentSerializer, CommentCreateSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """
    댓글 ViewSet

    - list: 댓글 목록 조회 (비회원 가능)
    - create: 댓글 작성 (회원만)
    - update: 댓글 수정 (본인 또는 관리자만)
    - destroy: 댓글 삭제 (본인 또는 관리자만, Soft Delete)
    """

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Comment.objects.filter(is_deleted=False)

        # 숨김 댓글은 관리자만 조회
        if not (self.request.user.is_authenticated and self.request.user.is_admin):
            queryset = queryset.filter(is_hidden=False)

        # 콘텐츠별 필터
        content_id = self.request.query_params.get('content_id', None)
        if content_id:
            queryset = queryset.filter(content_id=content_id, parent__isnull=True)

        return queryset.select_related('author', 'content').prefetch_related('replies')

    def get_serializer_class(self):
        if self.action == 'create':
            return CommentCreateSerializer
        return CommentSerializer

    def perform_update(self, serializer):
        """댓글 수정 권한 체크"""
        instance = self.get_object()
        if not (self.request.user == instance.author or self.request.user.is_admin):
            return Response(
                {"detail": "권한이 없습니다."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        """댓글 삭제 (Soft Delete)"""
        instance = self.get_object()

        if not (request.user == instance.author or request.user.is_admin):
            return Response(
                {"detail": "권한이 없습니다."},
                status=status.HTTP_403_FORBIDDEN
            )

        instance.is_deleted = True
        instance.save()

        return Response(
            {"detail": "댓글이 삭제되었습니다."},
            status=status.HTTP_204_NO_CONTENT
        )

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def hide(self, request, pk=None):
        """댓글 숨김/복구 (관리자만)"""
        if not request.user.is_admin:
            return Response(
                {"detail": "권한이 없습니다."},
                status=status.HTTP_403_FORBIDDEN
            )

        comment = self.get_object()
        comment.is_hidden = not comment.is_hidden
        comment.save()

        return Response(
            {"detail": f"댓글이 {'숨김' if comment.is_hidden else '복구'}되었습니다."},
            status=status.HTTP_200_OK
        )
