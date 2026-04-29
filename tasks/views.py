from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic
from django_filters.views import FilterView

from . import flashes
from .filters import TaskFilter
from .forms import TaskForm
from .mixins import UserAuthorTaskMixin
from .models import Label, Status, Task

SUCCESS_URL_STATUS = reverse_lazy('tasks:status_list')
SUCCESS_URL_TASK = reverse_lazy('tasks:task_list')
SUCCESS_URL_LABEL = reverse_lazy('tasks:label_list')


class StatusListView(LoginRequiredMixin, generic.ListView):
    model = Status
    template_name = 'statuses/list.html'
    context_object_name = 'statuses'


class StatusCreateView(LoginRequiredMixin, generic.CreateView):
    model = Status
    fields = ['name']
    template_name = 'statuses/form.html'
    success_url = SUCCESS_URL_STATUS

    def form_valid(self, form):
        messages.success(self.request, flashes.STATUS_CREATE)
        return super().form_valid(form)


class StatusUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Status
    fields = ['name']
    template_name = 'statuses/form.html'
    success_url = SUCCESS_URL_STATUS

    def form_valid(self, form):
        messages.success(self.request, flashes.STATUS_UPDATE)
        return super().form_valid(form)


class StatusDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Status
    template_name = 'statuses/delete.html'
    success_url = SUCCESS_URL_STATUS
    
    def post(self, request, *args, **kwargs):
        if self.get_object().task_set.exists():
            messages.error(request, flashes.STATUS_DELETE_ERROR)
            return redirect('tasks:status_list')
        messages.success(request, flashes.STATUS_DELETE)
        return super().post(request, *args, **kwargs)


class TaskListView(LoginRequiredMixin, FilterView):
    model = Task
    template_name = 'tasks/list.html'
    context_object_name = 'tasks'
    filterset_class = TaskFilter


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/form.html'
    success_url = SUCCESS_URL_TASK

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, flashes.TASK_CREATE)
        return super().form_valid(form)
    

class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/form.html'
    success_url = SUCCESS_URL_TASK

    def form_valid(self, form):
        messages.success(self.request, flashes.TASK_UPDATE)
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
    success_url = SUCCESS_URL_TASK

    def post(self, request, *args, **kwargs):
        if self.get_object().author != request.user:
            messages.error(request, flashes.TASK_DELETE_ERROR)
            return redirect('tasks:task_list')
        messages.success(request, flashes.TASK_DELETE)
        return super().post(request, *args, **kwargs)


class LabelListView(LoginRequiredMixin, generic.ListView):
    model = Label
    template_name = 'labels/list.html'
    context_object_name = 'labels'


class LabelCreateView(LoginRequiredMixin, generic.CreateView):
    model = Label
    fields = ['name']
    template_name = 'labels/form.html'
    success_url = SUCCESS_URL_LABEL

    def form_valid(self, form):
        messages.success(self.request, flashes.LABEL_CREATE)
        return super().form_valid(form)


class LabelUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Label
    fields = ['name']
    template_name = 'labels/form.html'
    success_url = SUCCESS_URL_LABEL

    def form_valid(self, form):
        messages.success(self.request, flashes.LABEL_UPDATE)
        return super().form_valid(form)


class LabelDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Label
    template_name = 'labels/delete.html'
    success_url = SUCCESS_URL_LABEL

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.tasks.exists():
            messages.error(
                request, 
                flashes.LABEL_DELETE_ERROR
            )
            return redirect('tasks:label_list')

        messages.success(request, flashes.LABEL_DELETE)
        return super().post(request, *args, **kwargs)
