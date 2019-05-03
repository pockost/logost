from django.urls import path

from .views import (
    ClientServerCreateView,
    ClientServerDeleteView,
    ClientServerDetailView,
    ClientServerListView,
    ClientServerSendLogView,
    ClientServerUpdateView
)

urlpatterns = [
    path(
        '<int:pk>',
        ClientServerDetailView.as_view(),
        name='client-server-detail'),
    path(
        'edit/<int:pk>',
        ClientServerUpdateView.as_view(),
        name='client-server-edit'),
    path(
        'delete/<int:pk>',
        ClientServerDeleteView.as_view(),
        name='client-server-delete'),
    path(
        'send-log/<int:pk>',
        ClientServerSendLogView.as_view(),
        name='client-server-send-log'),
    path(
        'create',
        ClientServerCreateView.as_view(),
        name='client-server-create'),
    path('', ClientServerListView.as_view(), name='client-server-list'),
]
