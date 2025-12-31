from rest_framework import serializers
from .models import Board, Post, PostReply


class BoardSerializer(serializers.ModelSerializer):
    """게시판 Serializer"""

    posts_count = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = ['id', 'name', 'board_type', 'description', 'posts_count']

    def get_posts_count(self, obj):
        return obj.posts.filter(is_deleted=False).count()


class PostReplySerializer(serializers.ModelSerializer):
    """게시글 답글 Serializer"""

    author_name = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = PostReply
        fields = ['id', 'post', 'author', 'author_name', 'content', 'created_at', 'updated_at']
        read_only_fields = ['author', 'created_at', 'updated_at']


class PostListSerializer(serializers.ModelSerializer):
    """게시글 목록용 Serializer"""

    board_name = serializers.CharField(source='board.name', read_only=True)
    board_type = serializers.CharField(source='board.board_type', read_only=True)
    author_name = serializers.CharField(source='author.username', read_only=True)
    replies_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'board', 'board_name', 'board_type', 'author', 'author_name',
            'title', 'status', 'is_pinned', 'view_count',
            'replies_count', 'created_at', 'updated_at'
        ]

    def get_replies_count(self, obj):
        return obj.admin_replies.count()


class PostDetailSerializer(serializers.ModelSerializer):
    """게시글 상세용 Serializer"""

    board_name = serializers.CharField(source='board.name', read_only=True)
    board_type = serializers.CharField(source='board.board_type', read_only=True)
    author_name = serializers.CharField(source='author.username', read_only=True)
    admin_replies = PostReplySerializer(many=True, read_only=True)
    can_edit = serializers.SerializerMethodField()
    can_delete = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'board', 'board_name', 'board_type', 'author', 'author_name',
            'title', 'content', 'status', 'is_pinned', 'view_count',
            'admin_replies', 'created_at', 'updated_at',
            'can_edit', 'can_delete'
        ]

    def get_can_edit(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        return obj.author == request.user or request.user.is_admin

    def get_can_delete(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        return obj.author == request.user or request.user.is_admin


class PostCreateUpdateSerializer(serializers.ModelSerializer):
    """게시글 생성/수정용 Serializer"""

    board_type = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Post
        fields = ['id', 'board', 'board_type', 'title', 'content', 'status']
        extra_kwargs = {
            'board': {'required': False},
            'id': {'read_only': True}
        }

    def validate(self, attrs):
        request = self.context.get('request')

        # board_type으로 board 찾기
        if 'board_type' in attrs:
            board_type = attrs.pop('board_type')
            try:
                board = Board.objects.get(board_type=board_type, is_active=True)
                attrs['board'] = board
            except Board.DoesNotExist:
                raise serializers.ValidationError(f"게시판을 찾을 수 없습니다: {board_type}")

        # 공지사항은 관리자만 작성 가능
        if attrs.get('board') and attrs['board'].board_type == Board.BoardType.NOTICE:
            if not request.user.is_admin:
                raise serializers.ValidationError("공지사항은 관리자만 작성할 수 있습니다.")

        return attrs
