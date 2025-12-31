from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    """댓글 Serializer"""

    author_name = serializers.CharField(source='author.username', read_only=True)
    replies_count = serializers.IntegerField(read_only=True)
    replies = serializers.SerializerMethodField()
    can_edit = serializers.SerializerMethodField()
    can_delete = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id', 'content', 'author', 'author_name', 'parent',
            'text', 'url_link', 'is_admin_reply', 'is_hidden', 'is_deleted',
            'created_at', 'updated_at', 'replies_count', 'replies',
            'can_edit', 'can_delete'
        ]
        read_only_fields = ['author', 'is_admin_reply', 'created_at', 'updated_at']

    def get_replies(self, obj):
        """답글 조회 (1depth만)"""
        if obj.parent is None:  # 최상위 댓글만 답글 표시
            replies = obj.replies.filter(is_deleted=False, is_hidden=False)
            return CommentSerializer(replies, many=True, context=self.context).data
        return []

    def get_can_edit(self, obj):
        """수정 권한 체크"""
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        return obj.author == request.user or request.user.is_admin

    def get_can_delete(self, obj):
        """삭제 권한 체크"""
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        return obj.author == request.user or request.user.is_admin


class CommentCreateSerializer(serializers.ModelSerializer):
    """댓글 생성용 Serializer"""

    class Meta:
        model = Comment
        fields = ['content', 'parent', 'text', 'url_link']

    def validate(self, attrs):
        """댓글 작성 권한 체크"""
        request = self.context.get('request')
        if not request.user.is_authenticated:
            raise serializers.ValidationError("로그인이 필요합니다.")

        if not request.user.can_comment:
            raise serializers.ValidationError("댓글 작성 권한이 없습니다.")

        return attrs

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['author'] = request.user

        # 관리자 답글 여부
        if request.user.is_admin and validated_data.get('parent'):
            validated_data['is_admin_reply'] = True

        return super().create(validated_data)
