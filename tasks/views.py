from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from .models import Status


class StatusListView(LoginRequiredMixin, generic.ListView):
    model = Status
    template_name = 'statuses/list.html'
    context_object_name = 'statuses'


class StatusCreateView(LoginRequiredMixin, generic.CreateView):
    model = Status
    fields = ['name']
    template_name = 'statuses/create_update.html'
    success_url = reverse_lazy('tasks:status_list')

    def form_valid(self, form):
        messages.success(self.request, 'Статус успешно создан')
        return super().form_valid(form)


class StatusUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Status
    fields = ['name']
    template_name = 'statuses/create_update.html'
    success_url = reverse_lazy('tasks:status_list')

    def form_valid(self, form):
        messages.success(self.request, 'Статус успешно изменён')
        return super().form_valid(form)


class StatusDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Status
    template_name = 'statuses/delete.html'
    success_url = reverse_lazy('tasks:status_list')
    
    def post(self, request, *args, **kwargs):
        messages.success(request, 'Статус успешно удалён')
        return super().post(request, *args, **kwargs)
