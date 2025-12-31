from django.apps import AppConfig


class ContentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.contents'
    verbose_name = '교육 콘텐츠'

    def ready(self):
        """앱이 준비되면 시그널 등록"""
        # 시그널 임시 비활성화 - Redis/Celery 없이 테스트
        # import apps.contents.signals
        pass
