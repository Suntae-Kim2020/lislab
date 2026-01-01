from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, MailingPreferenceViewSet
from .statistics import admin_statistics
from .social_auth import kakao_login, complete_social_signup, kakao_message_connect

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'mailing-preferences', MailingPreferenceViewSet, basename='mailing-preference')

urlpatterns = [
    path('', include(router.urls)),
    path('statistics/', admin_statistics, name='admin-statistics'),
    path('auth/kakao/callback/', kakao_login, name='kakao-login'),
    path('auth/social/complete/', complete_social_signup, name='complete-social-signup'),
    path('auth/kakao/message/connect/', kakao_message_connect, name='kakao-message-connect'),
]
