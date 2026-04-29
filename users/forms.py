from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import User


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'username', 'password1', 'password2',
        ]
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'username': 'Имя пользователя',
        }
        help_texts = {
            'username': '''
                Обязательное поле. Не более 150 символов. 
                Только буквы, цифры и символы @/./+/-/_,
            ''',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = 'Пароль'
        self.fields['password2'].label = 'Подтверждение пароля'
        self.fields['password1'].help_text = '''
            Ваш пароль должен содержать как минимум 3 символа.
        '''
        self.fields['password2'].help_text = '''
            Для подтверждения введите пароль ещё раз.
        '''


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'username': 'Имя пользователя',
        }
        help_texts = {
            'username': '''
                Обязательное поле. Не более 150 символов. 
                Только буквы, цифры и символы @/./+/-/_.',
            '''
        }


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].label = 'Имя пользователя'
        self.fields['password'].label = 'Пароль'
