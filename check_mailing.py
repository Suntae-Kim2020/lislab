from apps.accounts.models import User, MailingPreference

prefs = MailingPreference.objects.filter(enabled=True, frequency='IMMEDIATE')
print(f'Users with IMMEDIATE notifications: {prefs.count()}')
for p in prefs:
    cats = list(p.selected_categories.values_list('name', flat=True))
    print(f'  - {p.user.username} ({p.user.email}): all_categories={p.all_categories}, categories={cats}')
