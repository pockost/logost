from django.urls import path

from . import views

urlpatterns = [
    path(
        'syslog/create',
        views.SyslogLoggerServerCreateView.as_view(),
        name='logger-server-syslog-create'),
    path(
        'syslog/<int:pk>',
        views.SyslogLoggerServerDetailView.as_view(),
        name='logger-server-syslog-detail'),
    path(
        'create',
        views.LoggerServerCreateView.as_view(),
        name='logger-server-create'),
    path('', views.LoggerServerListView.as_view(), name='logger-server-list'),
]
