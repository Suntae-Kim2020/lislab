import json
from apps.contents.models import Favorite, Content
from apps.accounts.models import User
from apps.contents.serializers import FavoriteSerializer
from django.test import RequestFactory

# 사용자 가져오기
user = User.objects.get(username='givemechance')

# 즐겨찾기 조회
favorites = Favorite.objects.filter(
    user=user
).select_related(
    'content__category',
    'content__author'
).prefetch_related(
    'content__tags'
)

print(f'Found {favorites.count()} favorites')

# Serializer로 변환
factory = RequestFactory()
request = factory.get('/api/contents/favorites/')
request.user = user

serializer = FavoriteSerializer(favorites, many=True, context={'request': request})
data = serializer.data

print('\nSerialized data:')
print(json.dumps(data, indent=2, ensure_ascii=False))
