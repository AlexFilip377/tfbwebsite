from django.urls import path
from . import views
from .views import create_notifications, login_user
from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='home'),
    path('register', views.register, name='register'),
    path('search', views.search, name='search'),
    path('membership_list', views.membership_list, name='membership_list'),
    path('notifications', views.notifications, name='notifications'),
    path('create_notifications', lambda request: (create_notifications(), redirect('notifications'))),
    path('mark_notification_as_read/<int:notification_id>/', views.mark_notification_as_read, name='mark_notification_as_read'),
    path('login/', login_user, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout')
]
