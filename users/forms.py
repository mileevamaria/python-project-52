from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import User

FIELD_USERNAME__NAME = 'Имя пользователя'


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'username', 'password1', 'password2',
        ]
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'username': FIELD_USERNAME__NAME,
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
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput,
        required=False
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput,
        required=False
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'username': FIELD_USERNAME__NAME,
        }

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password1')
        p2 = cleaned_data.get('password2')

        if p1 or p2:
            if p1 != p2:
                raise forms.ValidationError('Пароли не совпадают')
            if len(p1) < 3:
                raise forms.ValidationError(
                    'Пароль должен быть не менее 3 символов')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password1')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].label = FIELD_USERNAME__NAME
        self.fields['password'].label = 'Пароль'
