from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.db.models import Q
from .models import Category, Tag, Content, ContentVersion, Favorite
from .serializers import (
    CategorySerializer,
    TagSerializer,
    ContentListSerializer,
    ContentDetailSerializer,
    ContentCreateUpdateSerializer,
    ContentVersionSerializer,
    FavoriteSerializer
)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """카테고리 ViewSet (읽기 전용)"""

    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = None  # 카테고리는 페이지네이션 비활성화 (전체 목록 반환)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """태그 ViewSet (읽기 전용)"""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ContentViewSet(viewsets.ModelViewSet):
    """
    콘텐츠 ViewSet

    - list: 콘텐츠 목록 조회 (비회원 가능)
    - retrieve: 콘텐츠 상세 조회 (비회원 가능, 조회수 증가)
    - create: 콘텐츠 생성 (관리자만)
    - update: 콘텐츠 수정 (관리자만)
    - destroy: 콘텐츠 삭제 (관리자만, Soft Delete)
    """

    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = Content.objects.filter(is_deleted=False)

        # 비관리자는 공개 콘텐츠만 조회
        if not (self.request.user.is_authenticated and self.request.user.is_admin):
            queryset = queryset.filter(status=Content.Status.PUBLISHED)

        # 검색
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(summary__icontains=search) |
                Q(tags__name__icontains=search)
            ).distinct()

        # 카테고리 필터 (상위 카테고리 또는 하위 카테고리)
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(
                Q(category__slug=category) | Q(category__parent__slug=category)
            )

        # 태그 필터 (slug 또는 name으로 검색)
        tag = self.request.query_params.get('tag', None)
        if tag:
            queryset = queryset.filter(
                Q(tags__slug=tag) | Q(tags__name=tag)
            ).distinct()

        # 난이도 필터
        difficulty = self.request.query_params.get('difficulty', None)
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)

        return queryset.select_related('category', 'author').prefetch_related('tags')

    def get_serializer_class(self):
        if self.action == 'list':
            return ContentListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ContentCreateUpdateSerializer
        return ContentDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        """콘텐츠 상세 조회 시 조회수 증가"""
        instance = self.get_object()
        instance.view_count += 1
        instance.save(update_fields=['view_count'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def perform_create(self, serializer):
        """콘텐츠 생성 시 작성자 자동 설정"""
        if not self.request.user.is_admin:
            return Response(
                {"detail": "권한이 없습니다."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        """콘텐츠 수정 시 권한 체크"""
        if not self.request.user.is_admin:
            return Response(
                {"detail": "권한이 없습니다."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        """콘텐츠 삭제 (Soft Delete)"""
        if not request.user.is_admin:
            return Response(
                {"detail": "권한이 없습니다."},
                status=status.HTTP_403_FORBIDDEN
            )

        instance = self.get_object()
        instance.is_deleted = True
        instance.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def favorite(self, request, slug=None):
        """즐겨찾기 등록/해제"""
        content = self.get_object()

        favorite, created = Favorite.objects.get_or_create(
            user=request.user,
            content=content
        )

        if not created:
            favorite.delete()
            return Response(
                {"detail": "즐겨찾기가 해제되었습니다."},
                status=status.HTTP_200_OK
            )

        return Response(
            {"detail": "즐겨찾기에 등록되었습니다."},
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=['get'])
    def versions(self, request, slug=None):
        """콘텐츠 버전 이력 조회"""
        content = self.get_object()
        versions = content.versions.all()
        serializer = ContentVersionSerializer(versions, many=True)
        return Response(serializer.data)


class FavoriteViewSet(viewsets.ReadOnlyModelViewSet):
    """즐겨찾기 ViewSet"""

    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(
            user=self.request.user
        ).select_related(
            'content__category',
            'content__author'
        ).prefetch_related(
            'content__tags'
        )
