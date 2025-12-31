from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MailingListViewSet, EmailCampaignViewSet

router = DefaultRouter()
router.register(r'mailing', MailingListViewSet, basename='mailing')
router.register(r'campaigns', EmailCampaignViewSet, basename='campaign')

urlpatterns = [
    path('', include(router.urls)),
]
