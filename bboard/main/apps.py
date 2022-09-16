from django.apps import AppConfig
from django.dispatch import Signal
from .utilities import send_activation_notification

#сигнал
user_registered = Signal(providing_args=['instance'])


def user_registered_dispatcher(sender, **kwargs):
    """Функция обработчик сигнала"""
    send_activation_notification(kwargs['instance'])

#привязка обработчика к сигналу
user_registered.connect(user_registered_dispatcher)


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'
    verbose_name = 'Доска объявлений'
