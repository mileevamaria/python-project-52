from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic

from .forms import UserRegisterForm, UserUpdateForm
from .mixins import IsSelfUserMixin


class UserListView(generic.ListView):
    model = User
    template_name = 'users/list.html'
    context_object_name = 'users'


class UserRegisterView(generic.CreateView):
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        messages.success(self.request, 'Пользователь успешно зарегистрирован')
        return super().form_valid(form)


class UserUpdateView(IsSelfUserMixin, generic.UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('users:list')

    def form_valid(self, form):
        messages.success(self.request, 'Пользователь успешно изменён')
        return super().form_valid(form)


class UserDeleteView(IsSelfUserMixin, generic.DeleteView):
    model = User
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users:list')

    def form_valid(self, form):
        messages.success(self.request, 'Пользователь успешно удален')
        return super().form_valid(form)


class UserLoginView(generic.FormView):
    form_class = AuthenticationForm
    template_name = 'users/login.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        login(self.request, form.get_user())
        messages.success(self.request, 'Вы залогинены')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Неверный логин или пароль')
        return super().form_invalid(form)


class UserLogoutView(generic.View):
    def post(self, request):
        logout(request)
        messages.success(self.request, 'Вы разлогинены')
        return redirect('users:login')
