from django.db import models
from django.contrib.auth.models import AbstractUser


class AdvUser(AbstractUser):
    """Класс - модель пользователя User с дополнительными данными о пользователе"""
    is_activated = models.BooleanField(default=True, db_index=True,
                                       verbose_name='Активация пройдена?')
    send_messages = models.BooleanField(default=True, verbose_name='Высылать оповещения о новых комментариях?')

    class Meta(AbstractUser.Meta):
        pass


class Rubric(models.Model):
    """Класс - модель рубрик"""
    name = models.CharField(max_length=25, db_index=True, unique=True,
                            verbose_name='Название')
    order = models.SmallIntegerField(default=0, db_index=True,
                                     verbose_name='Порядок')
    super_rubric = models.ForeignKey('SuperRubric',
                                     on_delete=models.PROTECT, null=True, blank=True,
                                     verbose_name='Надрубрика')


class SuperRubricManager(models.Manager):
    """Класс - модель диспетчер записей для изменения состава обрабатываемых
    моделью SuperRubric записей"""

    def get_queryset(self):
        """Функции для указания условий фильтрации записей.Будет выбирать только записи
        с пустым полем super_rubric, то есть надрубрики"""
        return super().get_queryset().filter(super_rubric__isnull=True)


class SuperRubric(Rubric):
    """Класс - прокси-модель для работы с надрубриками.Данная прокси-модель
    позволяет менять функциональность модели"""
    objects = SuperRubricManager()

    def __str__(self):
        """Функция, генерирующая название надрубрики"""
        return self.name

    class Meta:
        proxy = True
        ordering = ('order', 'name')
        verbose_name = 'Надрубрика'
        verbose_name_plural = 'Надрубрики'


class SubRubricManager(models.Manager):
    """Класс - модель диспетчер записей для изменения состава обрабатываемых
    моделью SubRubric записей"""

    def get_queryset(self):
        return super().get_queryset().filter(super_rubric__isnull=False)


class SubRubric(Rubric):
    """Класс - модель подрубрик"""
    objects = SubRubricManager()

    def __str__(self):
        """Функция, результатом которой является строковое представление:
        название надрубрики - название подрубрики"""
        return '%s -%s' % (self.super_rubric.name, self.name)

    class Meta:
        proxy = True
        ordering = ('super_rubric__order','super_rubric__name','order',
                    'name')
        verbose_name = 'Подрубрика'
        verbose_name_plural = 'Подрубрики'
