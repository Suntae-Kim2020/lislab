from apps.accounts.models import User
from apps.contents.models import Content, Favorite
from django.db.models import Count

print("=== Testing Statistics Queries ===\n")

# 1. Test admin user
admin = User.objects.filter(role='ADMIN').first()
print(f"1. Admin user: {admin.username if admin else 'None'}")
print(f"   is_admin: {admin.is_admin if admin else 'N/A'}\n")

# 2. Test content favorites
print("2. Testing favorite count query...")
try:
    top_favorited = Content.objects.annotate(
        favorite_count=Count('favorites')
    ).filter(
        favorite_count__gt=0
    ).order_by('-favorite_count')[:5]

    for content in top_favorited:
        print(f"   - {content.title}: {content.favorite_count} favorites")
except Exception as e:
    print(f"   ERROR: {e}\n")

# 3. Test viewed contents
print("\n3. Testing view count query...")
try:
    top_viewed = Content.objects.filter(
        view_count__gt=0
    ).order_by('-view_count')[:5]

    for content in top_viewed:
        print(f"   - {content.title}: {content.view_count} views")
except Exception as e:
    print(f"   ERROR: {e}")

# 4. Test user statistics
print("\n4. Testing user statistics...")
try:
    total_users = User.objects.filter(is_active=True).count()
    print(f"   - Total users: {total_users}")

    users_by_type = User.objects.filter(
        is_active=True
    ).values('user_type').annotate(
        count=Count('id')
    )

    for item in users_by_type:
        print(f"   - {item['user_type']}: {item['count']}")
except Exception as e:
    print(f"   ERROR: {e}")

print("\n=== Test Complete ===")
