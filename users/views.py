from django.contrib import messages
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic

from . import flashes
from .forms import UserLoginForm, UserRegisterForm, UserUpdateForm
from .mixins import IsSelfUserMixin
from .models import User

ROUTE_LIST = 'users:list'
ROUTE_LOGIN = 'users:login'


class UserListView(generic.ListView):
    model = User
    template_name = 'users/list.html'
    context_object_name = 'users'


class UserRegisterView(generic.CreateView):
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy(ROUTE_LOGIN)

    def form_valid(self, form):
        messages.success(self.request, flashes.USER_REGISTER)
        return super().form_valid(form)
    
    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)


class UserUpdateView(IsSelfUserMixin, generic.UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/update.html'
    success_url = reverse_lazy(ROUTE_LIST)

    def form_valid(self, form):
        messages.success(self.request, flashes.USER_UPDATE)
        return super().form_valid(form)


class UserDeleteView(IsSelfUserMixin, generic.DeleteView):
    model = User
    template_name = 'users/delete.html'
    success_url = reverse_lazy(ROUTE_LIST)

    def form_valid(self, form):
        if self.request.user.created_tasks.exists():
            messages.error(self.request, flashes.USER_DELETE_ERROR)
            return redirect(ROUTE_LIST)

        messages.success(self.request, flashes.USER_DELETE)
        return super().form_valid(form)


class UserLoginView(generic.FormView):
    form_class = UserLoginForm
    template_name = 'users/login.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        login(self.request, form.get_user())
        messages.success(self.request, flashes.USER_LOGIN)
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, flashes.USER_INVALID_CREDENTIALS)
        return super().form_invalid(form)


class UserLogoutView(generic.View):
    def post(self, request):
        logout(request)
        messages.success(self.request, flashes.USER_LOGOUT)
        return redirect(ROUTE_LOGIN)
