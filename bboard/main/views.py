from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from .models import AdvUser
from .forms import ChangeInfoFormUser
from django.contrib.auth.views import PasswordChangeView
from django.views.generic.edit import CreateView
from .forms import RegisterFormUser
from django.views.generic.base import TemplateView
from django.core.signing import BadSignature
from .utilities import signer
from django.views.generic.edit import DeleteView
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.views import PasswordResetDoneView
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.views import PasswordResetCompleteView


class BbLoginView(LoginView):
    template_name = 'main/login.html'


class BbLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'main/logout.html'


def index(request):
    return render(request, 'main/index.html')


def other_page(request, page):
    try:
        template = get_template('main/' + page + '.html')
    except TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request))


@login_required
def profile(request):
    return render(request, 'main/profile.html')


class ChangeInfoViewUser(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = AdvUser
    template_name = 'main/change_user_info.html'
    form_class = ChangeInfoFormUser
    success_url = reverse_lazy('main:profile')
    success_message = 'Данные пользователя успешно изменены'

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class BbPasswordChangeView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    template_name = 'main/password_change.html'
    success_url = reverse_lazy('main:profile')
    success_message = 'Изменение пароля пользователя прошло успешно!'


class RegisterViewUser(CreateView):
    """Класс - контроллер для регистрации пользователя"""
    model = AdvUser
    template_name = 'main/register_user.html'
    form_class = RegisterFormUser
    success_url = reverse_lazy('main:register_done')


class RegisterViewDone(TemplateView):
    """Класс - контроллер, выводящий сообщение об успешной регистрации"""
    template_name = 'main/register_done.html'


def user_activate(request, sign):
    """Функция конроллер для активации нового пользователя"""
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'main/bad_signature.html')
    user = get_object_or_404(AdvUser, username=username)
    if user.is_activated:
        template = 'main/user_is_activated.html'
    else:
        template = 'main/activation_done.html'
        user.is_active = True
        user.is_activated = True
        user.save()
    return render(request, template)


class DeleteViewUser(LoginRequiredMixin, DeleteView):
    """Класс-контроллер, удаляющий текущего пользователя"""
    model = AdvUser
    template_name = 'main/delete_user.html'
    success_url = reverse_lazy('main:index')

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'Пользователь успешно удален')
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class PasswordViewReset(PasswordResetView):
    """Класс-контроллер. Запрос на сброс пароля"""
    template_name = 'main/reset_password.html'
    subject_template_name = 'email/reset_subject_email.txt'
    email_template_name = 'email/reset_email.txt'
    success_url = reverse_lazy('main:password_reset_done')


class PasswordResetViewDone(PasswordResetDoneView):
    """Класс-котнроллер. Уведомление о том что письмо о сбросе пароля отправлено на почту"""
    template_name = 'main/password_reset_done.html'


class PasswordResetViewConfirm(PasswordResetConfirmView):
    """Класс-контроллер. Сброс старого пароля"""
    template_name = 'main/password_reset_confirm.html'
    success_url = reverse_lazy('main:password_reset_complete')


class PasswordResetViewComplete(PasswordResetCompleteView):
    """Класс-контроллер. Уведомление об успешном сбросе пароля"""
    template_name = 'main/password_confirmed.html'
