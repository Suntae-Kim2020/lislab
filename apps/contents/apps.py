from django.apps import AppConfig


class ContentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.contents'
    verbose_name = '교육 콘텐츠'

    def ready(self):
        """앱이 준비되면 시그널 등록"""
        import apps.contents.signals
