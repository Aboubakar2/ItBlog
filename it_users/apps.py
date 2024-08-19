from django.apps import AppConfig


class ItUsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'it_users'

    def ready(self):
        import it_users.signals
