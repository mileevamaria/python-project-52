from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('users/', views.UserListView.as_view(), name='list'),
    path(
        'users/create/', 
        views.UserRegisterView.as_view(), 
        name='create',
    ),
    path(
        'users/<int:pk>/update/', 
        views.UserUpdateView.as_view(), 
        name='update',
    ),

    path(
        'users/<int:pk>/delete/', 
        views.UserDeleteView.as_view(),
        name='delete',
    ),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
]