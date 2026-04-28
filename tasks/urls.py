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
]
