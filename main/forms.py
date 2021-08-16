from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

from .models import AdvUser
from .apps import user_registered

class RegisterUserForm(forms.ModelForm):

    email = forms.EmailField(required=True, label='Адрес электронной почты')
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput, help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(label='Пароль (повторно)',
                                widget=forms.PasswordInput,
                                help_text='Введите тот же самый пароль еще раз для проверки')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password2'] != cd['password1']:
            raise ValidationError("Password don't match")

        return cd['password2']

    # def clean(self):
    #     super().clean()
    #     print(self.cleaned_data)
    #     password1 = self.cleaned_data['password1']
    #     password2 = self.cleaned_data['password2']
    #     if password1 and password2 and password1 != password2:
    #         errors = {'password2': ValidationError(
    #             'Введёные пароли не совпадают', code='password_mismatch'
    #         )}
    #         raise ValidationError(errors)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = False
        user.is_activated = False
        if commit:
            user.save()
        user_registered.send(RegisterUserForm, instance=user)
        return user

    class Meta:
        model = AdvUser
        fields = ('username', 'email', 'password1', 'password2',
                  'first_name', 'last_name', 'send_messages')


class ChangeUserInfoForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Адрес электронной почты')


    class Meta:
        model = AdvUser
        fields = ('username', 'email', 'first_name', 'last_name', 'send_messages')
