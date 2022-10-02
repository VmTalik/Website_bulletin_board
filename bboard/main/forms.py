from django import forms
from .models import AdvUser, SuperRubric, SubRubric
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from .apps import user_registered
from django.forms import inlineformset_factory
from .models import Bb, AdditionalImage


class ChangeInfoFormUser(forms.ModelForm):
    email = forms.EmailField(required=True, label='Электронная почта')

    class Meta:
        model = AdvUser
        fields = ('username', 'email', 'first_name', 'last_name', 'send_messages')


class RegisterFormUser(forms.ModelForm):
    email = forms.EmailField(required=True, label='Электронная почта')
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput,
                                help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(label='Повторно пароль', widget=forms.PasswordInput,
                                help_text='Введите пароль повторно')

    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        if password1:
            password_validation.validate_password(password1)
        return password1

    def clean(self):
        super().clean()
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            errors = {'password2': ValidationError('Ошибка. Введеные пароли разные!', code='password_mismatch')}
            raise ValidationError(errors)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = False
        user.is_activated = False
        if commit:
            user.save()
        user_registered.send(RegisterFormUser, instance=user)
        return user

    class Meta:
        model = AdvUser
        fields = ('username', 'email', 'password1', 'password2', 'first_name',
                  'last_name', 'send_messages')


class SubRubricForm(forms.ModelForm):
    """ Класс-форма для создания поля надрубрики (super_rubric) у подрубрик"""
    super_rubric = forms.ModelChoiceField(
        queryset=SuperRubric.objects.all(), empty_label=None,
        label='Надрубрика', required=True)

    class Meta:
        model = SubRubric
        fields = '__all__'


class SearchForm(forms.Form):
    """Класс - форма для поиска слов, введенных пользователем"""
    keyword = forms.CharField(required=False, max_length=25, label='')


class BbForm(forms.ModelForm):
    """Класс - форма для ввода объявления"""

    class Meta:
        model = Bb
        fields = '__all__'
        widgets = {'author': forms.HiddenInput}


"""Встроенный набор форм дополнительных иллюстраций"""
AIFormSet = inlineformset_factory(Bb, AdditionalImage, fields='__all__')
