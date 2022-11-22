

from django.apps import AppConfig


class HelpdeskConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'helpdesk'

    def ready(self, *args, **kwargs) -> None:
        import helpdesk.signals  # noqa
        super_ready = super().ready(*args, **kwargs)
        return super_ready
