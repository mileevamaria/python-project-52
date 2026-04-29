from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect

from . import flashes


class IsSelfUserMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user == self.get_object()

    def handle_no_permission(self):
        messages.error(self.request, flashes.USER_FORBIDDEN)
        return redirect('users:list')
