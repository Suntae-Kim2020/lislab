from apps.accounts.models import User

try:
    user = User.objects.get(username='givemechance')
    print(f"Username: {user.username}")
    print(f"Email: {user.email}")
    print(f"Is active: {user.is_active}")
    print(f"Is staff: {user.is_staff}")
    print(f"Is admin: {user.is_admin}")
    print(f"Role: {user.role}")

    # 암호 재설정
    user.set_password('l1i2s300!')
    user.save()
    print("\nPassword reset successfully!")

    # 암호 확인
    if user.check_password('l1i2s300!'):
        print("Password verification: SUCCESS")
    else:
        print("Password verification: FAILED")

except User.DoesNotExist:
    print("User 'givemechance' does not exist!")
