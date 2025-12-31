"""
Admin 계정 비밀번호 재설정 스크립트
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.accounts.models import User

# Admin 계정 확인
admin = User.objects.filter(username='admin').first()

if admin:
    print(f"✓ Admin user found: {admin.username} ({admin.email})")
    print(f"  - Is superuser: {admin.is_superuser}")
    print(f"  - Is staff: {admin.is_staff}")
    print(f"  - Is active: {admin.is_active}")

    # 비밀번호 재설정
    new_password = "admin123!@#"
    admin.set_password(new_password)

    # 관리자 권한 확인 및 설정
    if not admin.is_superuser:
        admin.is_superuser = True
        print("  ✓ Set as superuser")

    if not admin.is_staff:
        admin.is_staff = True
        print("  ✓ Set as staff")

    if not admin.is_active:
        admin.is_active = True
        print("  ✓ Set as active")

    admin.save()

    print(f"\n✅ Password reset successfully!")
    print(f"\nLogin credentials:")
    print(f"  - URL: http://localhost:8000/admin")
    print(f"  - Username: admin")
    print(f"  - Password: {new_password}")
else:
    print("❌ Admin user not found. Creating new admin user...")

    admin = User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin123!@#',
        name='관리자'
    )

    print(f"\n✅ Admin user created successfully!")
    print(f"\nLogin credentials:")
    print(f"  - URL: http://localhost:8000/admin")
    print(f"  - Username: admin")
    print(f"  - Password: admin123!@#")
