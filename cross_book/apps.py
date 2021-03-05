from django.apps import AppConfig


class CrossBookConfig(AppConfig):
    name = 'cross_book'

    def ready(self):
        import cross_book.signals
