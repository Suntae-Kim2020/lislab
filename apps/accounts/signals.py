from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()


@receiver(m2m_changed, sender=User.groups.through)
def sync_staff_on_group_change(sender, instance, action, pk_set, **kwargs):
    """작성자 그룹 배정/해제 시 is_staff 자동 설정"""
    if action not in ('post_add', 'post_remove', 'post_clear'):
        return

    from django.contrib.auth.models import Group
    writer_group = Group.objects.filter(name='작성자').first()
    if not writer_group:
        return

    is_writer = instance.groups.filter(pk=writer_group.pk).exists()

    # 슈퍼유저/관리자는 건드리지 않음
    if instance.is_superuser or instance.role == 'ADMIN':
        return

    if is_writer and not instance.is_staff:
        instance.is_staff = True
        instance.save(update_fields=['is_staff'])
    elif not is_writer and instance.is_staff:
        instance.is_staff = False
        instance.save(update_fields=['is_staff'])
