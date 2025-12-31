from apps.contents.models import Favorite
from apps.accounts.models import User
from django.utils import timezone
from datetime import timedelta

print("=== 전체 사용자 목록 ===")
for user in User.objects.all():
    fav_count = Favorite.objects.filter(user=user).count()
    print(f"{user.username} (ID: {user.id}): {fav_count}개")

print("\n=== 최근 30분 내 생성된 즐겨찾기 ===")
recent_time = timezone.now() - timedelta(minutes=30)
recent_favs = Favorite.objects.filter(created_at__gte=recent_time).select_related('user', 'content')

if recent_favs.exists():
    for fav in recent_favs:
        print(f"User: {fav.user.username}, Content: {fav.content.title}, Time: {fav.created_at}")
else:
    print("최근 30분 내 생성된 즐겨찾기 없음")

print("\n=== 모든 즐겨찾기 (최근 10개) ===")
all_favs = Favorite.objects.all().select_related('user', 'content').order_by('-created_at')[:10]
for fav in all_favs:
    print(f"ID: {fav.id}, User: {fav.user.username}, Content: {fav.content.slug}, Time: {fav.created_at}")
