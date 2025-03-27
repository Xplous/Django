from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from app.models import Partner


class AnketaForm(forms.Form):
    name = forms.CharField(label='Ваше имя', min_length=2, max_length=100)
    internet = forms.ChoiceField(
        label='Оцените сайт',
        choices=(
            ('1', 'Плохо'),
            ('2', 'Средне'),
            ('3', 'Хорошо'),
            ('4', 'Отлично')
        ),
        widget=forms.RadioSelect,
        initial=1
    )

    notice = forms.BooleanField(
        label='Получать новости сайта на e-mail',
        required=False
    )

    email = forms.EmailField(label='Ваш e-mail', min_length=7)

    message = forms.CharField(
        label='Коротко о себе',
        widget=forms.Textarea(attrs={'rows': 12, 'cols': 20})
    )
class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label=_("Имя пользователя"),
        help_text=_("Не более 150 символов. Разрешены только буквы, цифры и @/./+/-/_"),
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(),
        label=_("Пароль"),
        help_text=_("Пароль должен содержать хотя бы 8 символов и не быть полностью числовым.")
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(),
        label=_("Подтверждение пароля"),
        help_text=_("Введите тот же пароль для подтверждения.")
    )

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

class PartnerForm(forms.ModelForm):
    class Meta:
        model = Partner
        fields = ['name', 'description', 'logo']