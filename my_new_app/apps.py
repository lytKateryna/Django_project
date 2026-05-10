from django.apps import AppConfig


class MyNewAppConfig(AppConfig):
    name = 'my_new_app'

    def ready(self) -> None:
        from my_new_app import signals
        # return super().ready()