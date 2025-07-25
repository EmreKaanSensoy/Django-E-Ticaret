from django.apps import AppConfig


class TicaretappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'AppTicaret'

    def ready(self):
        import AppTicaret.signals
