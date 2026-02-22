from django.db import migrations


def create_initial_menus(apps, schema_editor):
    Menu = apps.get_model('contents', 'Menu')
    Category = apps.get_model('contents', 'Category')

    # 카테고리 slug → 카테고리 객체 매핑
    def get_cat(slug):
        try:
            return Category.objects.get(slug=slug)
        except Category.DoesNotExist:
            return None

    # 1) 알기쉬운 통계(작성중)
    Menu.objects.create(
        name='알기쉬운 통계(작성중)',
        category=get_cat('statistics'),
        order=10,
        is_active=True,
        show_subcategories=True,
    )

    # 2) 디지털도서관 (URL 기반, 하위에 카테고리별 항목)
    library = Menu.objects.create(
        name='디지털도서관',
        url='/contents',
        order=20,
        is_active=True,
        show_subcategories=False,
    )

    # 디지털도서관 하위 메뉴: 독립 메뉴로 분리된 카테고리 제외
    exclude_slugs = ['practice', 'statistics', 'special-lecture-a', 'special-lecture-b']
    lib_categories = Category.objects.filter(
        parent__isnull=True,
        is_active=True,
    ).exclude(slug__in=exclude_slugs).order_by('order', 'name')

    for i, cat in enumerate(lib_categories):
        Menu.objects.create(
            name=cat.name,
            category=cat,
            parent=library,
            order=(i + 1) * 10,
            is_active=True,
            show_subcategories=True,
        )

    # 3) 특강A(베타)
    Menu.objects.create(
        name='특강A(베타)',
        category=get_cat('special-lecture-a'),
        order=30,
        is_active=True,
        show_subcategories=True,
    )

    # 4) 특강B(베타)
    Menu.objects.create(
        name='특강B(베타)',
        category=get_cat('special-lecture-b'),
        order=40,
        is_active=True,
        show_subcategories=True,
    )

    # 5) 실습
    Menu.objects.create(
        name='실습',
        category=get_cat('practice'),
        order=50,
        is_active=True,
        show_subcategories=True,
    )

    # 6) 게시판
    Menu.objects.create(
        name='게시판',
        url='/boards',
        order=60,
        is_active=True,
        show_subcategories=False,
    )

    # 7) 소개 (드롭다운)
    about = Menu.objects.create(
        name='소개',
        order=70,
        is_active=True,
        show_subcategories=False,
    )

    Menu.objects.create(
        name='LIS Lab 소개',
        url='/about',
        parent=about,
        order=10,
        is_active=True,
    )

    Menu.objects.create(
        name='LIS Lab 사람들',
        url='/about/people',
        parent=about,
        order=20,
        is_active=True,
    )


def reverse_initial_menus(apps, schema_editor):
    Menu = apps.get_model('contents', 'Menu')
    Menu.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('contents', '0006_menu'),
    ]

    operations = [
        migrations.RunPython(create_initial_menus, reverse_initial_menus),
    ]
