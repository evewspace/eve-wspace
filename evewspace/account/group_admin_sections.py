from account.group_admin_section_registry import registry

registry.register('Group Settings', 'group_admin_profile.html', 'account.account_admin')
registry.register('Members', 'group_admin_users.html', 'account.account_admin')
