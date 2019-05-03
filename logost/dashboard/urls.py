from django.urls import path

from .views import ClientServerListView

urlpatterns = [
    path('', ClientServerListView.as_view(), name='client-server-list'),
]
