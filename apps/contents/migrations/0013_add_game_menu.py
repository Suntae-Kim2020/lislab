# 운영 DB에 '게임' 메뉴 카테고리를 자동 등록한다.
# url 필드를 채워 네비게이션 전용 메뉴로 동작 (Category.get_menu_url 참고).
from django.db import migrations


GAME_MENU_NAME = '게임'
GAME_MENU_URL = '/tools/cute-timer.html'


def add_game_menu(apps, schema_editor):
    Category = apps.get_model('contents', 'Category')
    Category.objects.update_or_create(
        name=GAME_MENU_NAME,
        defaults={
            'show_in_menu': True,
            'url': GAME_MENU_URL,
            'menu_order': 999,
            'is_active': True,
            'open_in_new_tab': False,
            'description': '',
        },
    )


def remove_game_menu(apps, schema_editor):
    Category = apps.get_model('contents', 'Category')
    Category.objects.filter(name=GAME_MENU_NAME, url=GAME_MENU_URL).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('contents', '0012_content_html_source_file'),
    ]

    operations = [
        migrations.RunPython(add_game_menu, remove_game_menu),
    ]
