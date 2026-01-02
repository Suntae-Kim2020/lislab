from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, MailingPreference
from apps.contents.models import Category


class UserSerializer(serializers.ModelSerializer):
    """사용자 정보 조회용 Serializer"""

    kakao_message_token = serializers.SerializerMethodField()
    has_kakao_message_token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'role', 'user_type', 'phone', 'organization', 'bio',
            'profile_image', 'is_email_verified', 'social_provider',
            'kakao_message_token', 'has_kakao_message_token', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'role', 'social_provider', 'kakao_message_token', 'has_kakao_message_token']

    def get_kakao_message_token(self, obj):
        """카카오 메시지 토큰 유무만 반환 (보안)"""
        return 'connected' if obj.kakao_message_token else None

    def get_has_kakao_message_token(self, obj):
        """카카오 메시지 토큰 보유 여부 (boolean)"""
        return bool(obj.kakao_message_token)


class UserRegistrationSerializer(serializers.ModelSerializer):
    """회원가입용 Serializer"""

    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True
    )

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password_confirm',
            'first_name', 'last_name', 'user_type', 'phone', 'organization'
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({
                "password": "비밀번호가 일치하지 않습니다."
            })
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """사용자 정보 수정용 Serializer"""

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'phone',
            'organization', 'bio', 'profile_image', 'user_type'
        ]


class PasswordChangeSerializer(serializers.Serializer):
    """비밀번호 변경용 Serializer"""

    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(
        required=True,
        write_only=True,
        validators=[validate_password]
    )
    new_password_confirm = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({
                "new_password": "비밀번호가 일치하지 않습니다."
            })
        return attrs


class MailingPreferenceSerializer(serializers.ModelSerializer):
    """메일링 설정 Serializer"""

    selected_category_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = MailingPreference
        fields = [
            'id', 'enabled', 'frequency', 'all_categories',
            'selected_categories', 'selected_category_ids',
            'kakao_notification_enabled',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'selected_categories']

    def get_selected_categories(self, obj):
        """선택된 카테고리 정보 반환"""
        return [
            {
                'id': cat.id,
                'name': cat.name,
                'slug': cat.slug
            }
            for cat in obj.selected_categories.all()
        ]

    def to_representation(self, instance):
        """응답 시 선택된 카테고리 정보 포함"""
        data = super().to_representation(instance)
        data['selected_categories'] = self.get_selected_categories(instance)
        return data

    def update(self, instance, validated_data):
        """메일링 설정 업데이트"""
        category_ids = validated_data.pop('selected_category_ids', None)

        # 기본 필드 업데이트
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # 선택 카테고리 업데이트
        if category_ids is not None:
            categories = Category.objects.filter(id__in=category_ids)
            instance.selected_categories.set(categories)

        return instance
