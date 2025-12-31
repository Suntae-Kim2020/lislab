from rest_framework import serializers
from .models import Category, Tag, Content, ContentVersion, Favorite


class CategorySerializer(serializers.ModelSerializer):
    """카테고리 Serializer"""

    children_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'parent', 'order', 'children_count']

    def get_children_count(self, obj):
        return obj.children.count()


class TagSerializer(serializers.ModelSerializer):
    """태그 Serializer"""

    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']


class ContentListSerializer(serializers.ModelSerializer):
    """콘텐츠 목록용 Serializer"""

    category_name = serializers.CharField(source='category.name', read_only=True)
    author_name = serializers.CharField(source='author.username', read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    is_favorited = serializers.SerializerMethodField()

    class Meta:
        model = Content
        fields = [
            'id', 'title', 'slug', 'summary', 'thumbnail',
            'category', 'category_name', 'tags',
            'author', 'author_name', 'status', 'version',
            'view_count', 'estimated_time', 'difficulty',
            'created_at', 'updated_at', 'is_favorited'
        ]

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Favorite.objects.filter(user=request.user, content=obj).exists()
        return False


class ContentDetailSerializer(serializers.ModelSerializer):
    """콘텐츠 상세용 Serializer"""

    category_name = serializers.CharField(source='category.name', read_only=True)
    author_name = serializers.CharField(source='author.username', read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    is_favorited = serializers.SerializerMethodField()
    favorite_count = serializers.SerializerMethodField()

    class Meta:
        model = Content
        fields = [
            'id', 'title', 'slug', 'summary', 'content_html',
            'category', 'category_name', 'tags',
            'author', 'author_name', 'status', 'version',
            'thumbnail', 'view_count', 'estimated_time', 'difficulty',
            'prerequisites', 'learning_objectives',
            'meta_description', 'meta_keywords',
            'created_at', 'updated_at', 'published_at',
            'is_favorited', 'favorite_count'
        ]

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Favorite.objects.filter(user=request.user, content=obj).exists()
        return False

    def get_favorite_count(self, obj):
        return obj.favorited_by.count()


class ContentCreateUpdateSerializer(serializers.ModelSerializer):
    """콘텐츠 생성/수정용 Serializer"""

    class Meta:
        model = Content
        fields = [
            'title', 'slug', 'summary', 'content_html',
            'category', 'tags', 'status', 'version',
            'thumbnail', 'estimated_time', 'difficulty',
            'prerequisites', 'learning_objectives',
            'meta_description', 'meta_keywords'
        ]

    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        content = Content.objects.create(**validated_data)
        content.tags.set(tags)
        return content


class ContentVersionSerializer(serializers.ModelSerializer):
    """콘텐츠 버전 Serializer"""

    created_by_name = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = ContentVersion
        fields = ['id', 'content', 'version', 'content_html', 'change_log', 'created_by', 'created_by_name', 'created_at']
        read_only_fields = ['created_at', 'created_by']


class FavoriteContentSerializer(serializers.ModelSerializer):
    """즐겨찾기용 콘텐츠 Serializer (is_favorited 필드 최적화)"""

    category_name = serializers.CharField(source='category.name', read_only=True)
    author_name = serializers.CharField(source='author.username', read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    is_favorited = serializers.SerializerMethodField()

    class Meta:
        model = Content
        fields = [
            'id', 'title', 'slug', 'summary', 'thumbnail',
            'category', 'category_name', 'tags',
            'author', 'author_name', 'status', 'version',
            'view_count', 'estimated_time', 'difficulty',
            'created_at', 'updated_at', 'is_favorited'
        ]

    def get_is_favorited(self, obj):
        # 즐겨찾기 목록에서는 항상 True
        return True


class FavoriteSerializer(serializers.ModelSerializer):
    """즐겨찾기 Serializer"""

    content = FavoriteContentSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'content', 'created_at']
        read_only_fields = ['created_at']
