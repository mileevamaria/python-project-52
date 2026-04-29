from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic

from .mixins import UserAuthorTaskMixin
from .models import Label, Status, Task


class StatusListView(LoginRequiredMixin, generic.ListView):
    model = Status
    template_name = 'statuses/list.html'
    context_object_name = 'statuses'


class StatusCreateView(LoginRequiredMixin, generic.CreateView):
    model = Status
    fields = ['name']
    template_name = 'statuses/form.html'
    success_url = reverse_lazy('tasks:status_list')

    def form_valid(self, form):
        messages.success(self.request, 'Статус успешно создан')
        return super().form_valid(form)


class StatusUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Status
    fields = ['name']
    template_name = 'statuses/form.html'
    success_url = reverse_lazy('tasks:status_list')

    def form_valid(self, form):
        messages.success(self.request, 'Статус успешно изменён')
        return super().form_valid(form)


class StatusDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Status
    template_name = 'statuses/delete.html'
    success_url = reverse_lazy('tasks:status_list')
    
    def post(self, request, *args, **kwargs):
        # TODO: удалить статус только если он не используется в задачах
        messages.success(request, 'Статус успешно удалён')
        return super().post(request, *args, **kwargs)


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    template_name = 'tasks/list.html'
    context_object_name = 'tasks'


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    fields = ['name', 'description', 'status', 'executor']
    template_name = 'tasks/form.html'
    success_url = reverse_lazy('tasks:task_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Задача успешно создана')
        return super().form_valid(form)
    

class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    fields = ['name', 'description', 'status', 'executor']
    template_name = 'tasks/form.html'
    success_url = reverse_lazy('tasks:task_list')

    def form_valid(self, form):
        messages.success(self.request, 'Задача успешно изменена')
        return super().form_valid(form)
    

class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    template_name = 'tasks/detail.html'
    context_object_name = 'task'


class TaskDeleteView(
    LoginRequiredMixin, UserAuthorTaskMixin, generic.DeleteView,
):
    model = Task
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy('tasks:task_list')

    def post(self, request, *args, **kwargs):
        messages.success(request, 'Задача успешно удалена')
        return super().post(request, *args, **kwargs)


class LabelListView(LoginRequiredMixin, generic.ListView):
    model = Label
    template_name = 'labels/list.html'
    context_object_name = 'labels'


class LabelCreateView(LoginRequiredMixin, generic.CreateView):
    model = Label
    fields = ['name']
    template_name = 'labels/form.html'
    success_url = reverse_lazy('tasks:label_list')

    def form_valid(self, form):
        messages.success(self.request, 'Метка успешно создана')
        return super().form_valid(form)


class LabelUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Label
    fields = ['name']
    template_name = 'labels/form.html'
    success_url = reverse_lazy('tasks:label_list')

    def form_valid(self, form):
        messages.success(self.request, 'Метка успешно изменена')
        return super().form_valid(form)


class LabelDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Label
    template_name = 'labels/delete.html'
    success_url = reverse_lazy('tasks:label_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.tasks.exists():
            messages.error(
                request, 
                'Невозможно удалить метку, потому что она используется',
            )
            return redirect('tasks:label_list')

        messages.success(request, 'Метка успешно удалена')
        return super().post(request, *args, **kwargs)
