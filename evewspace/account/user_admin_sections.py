from account.user_admin_section_registry import registry

registry.register('Account Settings', 'user_admin_profile.html', 'account.account_admin')
registry.register('Group Memberships', 'user_admin_groups.html', 'account.account_admin')
