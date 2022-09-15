from django.db import models
from django.contrib.auth.models import AbstractUser


class AdvUser(AbstractUser):
    is_activated = models.BooleanField(default=True, db_index=True,
                                       verbose_name='Активация пройдена?')
    send_messages = models.BooleanField(default=True, verbose_name='Высылать оповещения о новых комментариях?')

    class Meta(AbstractUser.Meta):
        pass
