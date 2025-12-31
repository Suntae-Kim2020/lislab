from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Board, Post, PostReply
from .serializers import (
    BoardSerializer,
    PostListSerializer,
    PostDetailSerializer,
    PostCreateUpdateSerializer,
    PostReplySerializer
)


class BoardViewSet(viewsets.ReadOnlyModelViewSet):
    """게시판 ViewSet (읽기 전용)"""

    queryset = Board.objects.filter(is_active=True)
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class PostViewSet(viewsets.ModelViewSet):
    """
    게시글 ViewSet

    - list: 게시글 목록 조회 (비회원 가능)
    - retrieve: 게시글 상세 조회 (비회원 가능, 조회수 증가)
    - create: 게시글 작성 (회원만)
    - update: 게시글 수정 (본인 또는 관리자만)
    - destroy: 게시글 삭제 (본인 또는 관리자만, Soft Delete)
    """

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Post.objects.filter(is_deleted=False)

        # 게시판 필터
        board_type = self.request.query_params.get('board_type', None)
        if board_type:
            queryset = queryset.filter(board__board_type=board_type)

        # 상태 필터 (관리자만)
        if self.request.user.is_authenticated and self.request.user.is_admin:
            post_status = self.request.query_params.get('status', None)
            if post_status:
                queryset = queryset.filter(status=post_status)

        # 검색
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(title__icontains=search)

        return queryset.select_related('board', 'author').prefetch_related('admin_replies')

    def get_serializer_class(self):
        if self.action == 'list':
            return PostListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return PostCreateUpdateSerializer
        return PostDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        """게시글 상세 조회 시 조회수 증가"""
        instance = self.get_object()
        instance.view_count += 1
        instance.save(update_fields=['view_count'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def perform_create(self, serializer):
        """게시글 생성 시 작성자 자동 설정"""
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        """게시글 수정 권한 체크"""
        instance = self.get_object()
        if not (self.request.user == instance.author or self.request.user.is_admin):
            return Response(
                {"detail": "권한이 없습니다."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        """게시글 삭제 (Soft Delete)"""
        instance = self.get_object()

        if not (request.user == instance.author or request.user.is_admin):
            return Response(
                {"detail": "권한이 없습니다."},
                status=status.HTTP_403_FORBIDDEN
            )

        instance.is_deleted = True
        instance.save()

        return Response(
            {"detail": "게시글이 삭제되었습니다."},
            status=status.HTTP_204_NO_CONTENT
        )

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def reply(self, request, pk=None):
        """관리자 답글 작성"""
        if not request.user.is_admin:
            return Response(
                {"detail": "권한이 없습니다."},
                status=status.HTTP_403_FORBIDDEN
            )

        post = self.get_object()
        serializer = PostReplySerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(post=post, author=request.user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
