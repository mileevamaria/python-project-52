from django.urls import include, path

from . import views

app_name = 'tasks'

CRUD_PATHS = {
    'create': 'create/',
    'update': '<int:pk>/update/',
    'delete': '<int:pk>/delete/',
    'list': '',
    'detail': '<int:pk>/',
}

urlpatterns = [
    path('statuses/', include([
        path(CRUD_PATHS['list'], views.StatusListView.as_view(), name='status_list'),
        path(CRUD_PATHS['create'], views.StatusCreateView.as_view(), name='status_create'),
        path(
            CRUD_PATHS['update'], 
            views.StatusUpdateView.as_view(), 
            name='status_update',
        ),
        path(
            CRUD_PATHS['delete'], 
            views.StatusDeleteView.as_view(), 
            name='status_delete',
        ),
    ])),
    path('tasks/', include([
        path(CRUD_PATHS['list'], views.TaskListView.as_view(), name='task_list'),
        path(CRUD_PATHS['detail'], views.TaskDetailView.as_view(), name='task_detail'),
        path(CRUD_PATHS['create'], views.TaskCreateView.as_view(), name='task_create'),
        path(
            CRUD_PATHS['update'],
            views.TaskUpdateView.as_view(),
            name='task_update',
        ),
        path(
            CRUD_PATHS['delete'],
            views.TaskDeleteView.as_view(),
            name='task_delete',
        ),
    ])),
    path('labels/', include([
        path(CRUD_PATHS['list'], views.LabelListView.as_view(), name='label_list'),
        path(CRUD_PATHS['create'], views.LabelCreateView.as_view(), name='label_create'),
        path(
            CRUD_PATHS['update'],
            views.LabelUpdateView.as_view(),
            name='label_update',
        ),
        path(
            CRUD_PATHS['delete'], 
            views.LabelDeleteView.as_view(), 
            name='label_delete',
        ),
    ])),
]
