from django.contrib import admin
from .models import AdvUser
from .utilities import send_activation_notification
import datetime
from .models import SuperRubric, SubRubric
from .forms import SubRubricForm
from .models import Bb, AdditionalImage
from .models import Comment


def send_activation_notifications(modeladmin, request, queryset):
    """Функция, с помощью которой пользователям осущевляется рассылка
    писем с предписаниями выполнить активацию"""
    for rec in queryset:
        if not rec.is_activated:
            send_activation_notification(rec)
    modeladmin.message_user(request, 'Электронные письма с требованиями отправлены')


send_activation_notifications.short_description = 'Отправление писем с требованиями об активации'


class NonactivatedFilter(admin.SimpleListFilter):
    """Вспомогательный класс, осущетвляет фильтрацию пользователей, выполнивших
    активацию, не выполнивших ее в течение трех дней и недели"""
    title = 'Активация пройдена?'
    parameter_name = 'actstate'

    def lookups(self, request, model_admin):
        return (
            ('activated', 'Прошли'),
            ('threedays', 'Не прошли уже более 3 дней'),
            ('week', 'Не прошли уже более недели'),

        )

    def queryset(self, request, queryset):
        val = self.value()
        if val == 'activated':
            return queryset.filter(is_active=True, is_activated=True)
        elif val == 'threedays':
            d = datetime.date.today() - datetime.timedelta(days=3)
            return queryset.filter(is_active=False, is_activated=False, date_joined__date__lt=d)
        elif val == 'week':
            d = datetime.date.today() - datetime.timedelta(weeks=1)
            return queryset.filter(is_active=False, is_activated=False, date_joined__date__lt=d)


class AdvUserAdmin(admin.ModelAdmin):
    """Класс редактор администрации сайта, для работы с зарегистрированными пользователями"""
    list_display = ('__str__', 'is_activated', 'date_joined')
    search_fields = ('username', 'email', 'firstname', 'lastname')
    list_filter = (NonactivatedFilter,)
    fields = (('username', 'email'), ('first_name', 'last_name'),
              ('send_messages', 'is_active', 'is_activated'),
              ('is_staff', 'is_superuser'), 'groups', 'user_permissions',
              ('last_login', 'date_joined'))
    readonly_fields = ('last_login', 'date_joined')
    actions = (send_activation_notifications,)


admin.site.register(AdvUser, AdvUserAdmin)


class SubRubricInline(admin.TabularInline):
    "Класс - редактор подрубрик административного сайта"
    model = SubRubric


class SuperRubricAdmin(admin.ModelAdmin):
    """Класс - редактор надрубрик административного сайта"""
    exclude = ('super_rubric',)
    inlines = (SubRubricInline,)


admin.site.register(SuperRubric, SuperRubricAdmin)


class SubRubricAdmin(admin.ModelAdmin):
    """Класс - редактор формы подрубрик SubRubricForm"""
    form = SubRubricForm


admin.site.register(SubRubric, SubRubricAdmin)


class AdditionalImageInline(admin.TabularInline):
    """Класс - встроенный редактор дополнительных иллюстраций"""
    model = AdditionalImage


class BbAdmin(admin.ModelAdmin):
    """Класс - редактор объявлений"""
    list_display = ('rubric', 'title', 'content', 'author', 'created_at')
    fields = (('rubric', 'author'), 'title', 'content', 'price',
              'contacts', 'image', 'is_active')
    inlines = (AdditionalImageInline,)


admin.site.register(Bb, BbAdmin)


class CommentAdmin(admin.ModelAdmin):
    """Класс - редактор комментариев"""
    list_display = ('bb', 'author', 'content', 'is_active', 'created_at')
    fields = (('bb', 'author'), 'content', 'is_active')


admin.site.register(Comment, CommentAdmin)
