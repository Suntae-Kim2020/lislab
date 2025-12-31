from apps.accounts.models import User
from rest_framework.authtoken.models import Token

user = User.objects.get(username='givemechance')
token, created = Token.objects.get_or_create(user=user)
print(f'Token: {token.key}')
