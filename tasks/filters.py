import django_filters

from .models import Label, Task


class TaskFilter(django_filters.FilterSet):
    labels = django_filters.ModelChoiceFilter(
        queryset=Label.objects.all(),
        label='Метка'
    )
    self_tasks = django_filters.BooleanFilter(
        method='filter_self_tasks',
        label='Только свои задачи'
    )

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels']

    def filter_self_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset
