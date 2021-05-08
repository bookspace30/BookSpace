from django.apps import AppConfig


# class AccountsConfig(AppConfig):
#     name = 'accounts'
#
#     def ready(self):
#         import accounts.signals


class StoreConfig(AppConfig):
    name = 'accounts'

    def ready(self):
        import accounts.signals
