from django.db import models
from django.contrib.auth.models import AbstractUser
from .utilities import get_timestamp_path


class AdvUser(AbstractUser):
    """Класс - модель пользователя User с дополнительными данными о пользователе"""
    is_activated = models.BooleanField(default=True, db_index=True,
                                       verbose_name='Активация пройдена?')
    send_messages = models.BooleanField(default=True, verbose_name='Высылать оповещения о новых комментариях?')

    def delete(self, *args, **kwargs):
        for bb in self.bb_set.all():
            bb.delete()
        super().delete(*args, **kwargs)

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
        ordering = ('super_rubric__order', 'super_rubric__name', 'order',
                    'name')
        verbose_name = 'Подрубрика'
        verbose_name_plural = 'Подрубрики'


class Bb(models.Model):
    """Класс - модель объявлений"""
    rubric = models.ForeignKey(SubRubric, on_delete=models.PROTECT, verbose_name='Рубрика')
    title = models.CharField(max_length=45, verbose_name='Объект продажи')
    content = models.TextField(verbose_name='Описание')
    price = models.FloatField(default=0, verbose_name='Цена')
    contacts = models.TextField(verbose_name='Контакты')
    image = models.ImageField(blank=True, upload_to=get_timestamp_path, verbose_name='Изображение')
    author = models.ForeignKey(AdvUser, on_delete=models.CASCADE, verbose_name='Автор объявления')
    is_active = models.BooleanField(default=True, db_index=True, verbose_name='Выводить в списке ?')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликовано')

    def delete(self, *args, **kwargs):
        """Функция, удаляющая дполнительные иллюстрации. При вызове данного метода
        возникает сигнал post_delete, обрабатываемый приложением django_cleanup"""
        for i in self.additionalimage_set.all():
            i.delete()
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Объявления'
        verbose_name = 'Объявление'
        ordering = ['-created_at']


class AdditionalImage(models.Model):
    """Класс - модель дополнительных иллюстраций"""
    bb = models.ForeignKey(Bb, on_delete=models.CASCADE, verbose_name='Объявление')
    image = models.ImageField(upload_to=get_timestamp_path, verbose_name='Изображение')

    class Meta:
        verbose_name_plural = 'Дополнительные иллюстрации'
        verbose_name = 'Дополнительная иллюстрация'


class Comment(models.Model):
    """Класс - модель комментарии посетителей сайта"""
    bb = models.ForeignKey(Bb, on_delete=models.CASCADE,
                           verbose_name='Объявление')
    author = models.CharField(max_length=35, verbose_name='Автор')
    content = models.TextField(verbose_name='Содержание')
    is_active = models.BooleanField(default=True, db_index=True,
                                    verbose_name='Вывести на экран ?')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True,
                                      verbose_name='Опубликовано')

    class Meta:
        verbose_name_plural = 'Комментарии'
        verbose_name = 'Комментарий'
        ordering = ['created_at']
