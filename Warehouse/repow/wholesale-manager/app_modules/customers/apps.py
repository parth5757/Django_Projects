from django.apps import AppConfig


class CustomersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_modules.customers'

    def ready(self):
        import app_modules.customers.signals
