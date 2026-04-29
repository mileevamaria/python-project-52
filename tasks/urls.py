from django.urls import path, include
from . import views

app_name = 'tasks'

urlpatterns = [
    path('statuses/', include([
        path('', views.StatusListView.as_view(), name='status_list'),
        path('create/', views.StatusCreateView.as_view(), name='status_create'),
        path(
            '<int:pk>/update/', 
            views.StatusUpdateView.as_view(), 
            name='status_update',
        ),
        path(
            '<int:pk>/delete/', 
            views.StatusDeleteView.as_view(), 
            name='status_delete',
        ),
    ])),
    path('tasks/', include([
        path('', views.TaskListView.as_view(), name='task_list'),
        path('<int:pk>/', views.TaskDetailView.as_view(), name='task_detail'),
        path('create/', views.TaskCreateView.as_view(), name='task_create'),
        path(
            '<int:pk>/update/',
            views.TaskUpdateView.as_view(),
            name='task_update',
        ),
        path(
            '<int:pk>/delete/',
            views.TaskDeleteView.as_view(),
            name='task_delete',
        ),
    ])),
]
