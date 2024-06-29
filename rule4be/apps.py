# apps.py
from django.apps import AppConfig


class Rule4beConfig(AppConfig):
    name = 'rule4be'

    def ready(self):
        import rule4be.signals
