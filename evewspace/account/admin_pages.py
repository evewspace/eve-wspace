from core.admin_page_registry import registry

registry.register('Users', 'user_admin.html', 'account.account_admin')
registry.register('Groups', 'group_admin.html', 'account.account_admin')
