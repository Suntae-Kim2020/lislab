from apps.contents.models import Favorite
from apps.accounts.models import User

print('Total favorites:', Favorite.objects.count())
print('\nFavorite records:')
for f in Favorite.objects.select_related('user', 'content').all()[:10]:
    print(f'  User: {f.user.username}, Content: {f.content.title}')

print('\nUsers:')
for u in User.objects.all()[:5]:
    fav_count = Favorite.objects.filter(user=u).count()
    print(f'  {u.username}: {fav_count} favorites')
