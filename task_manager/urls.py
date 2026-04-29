from django.contrib import admin
from django.urls import include, path

from .views import HomeView, test_error

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('test-error/', test_error, name='test_error'),
    path('admin/', admin.site.urls),
    path('', include('tasks.urls')),
    path('', include('users.urls')),
]
