from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from .models import LoggerServer, SyslogLoggerServer


class LoggerServerListView(ListView):

    model = LoggerServer
    fields = ['name']


class LoggerServerCreateView(CreateView):

    model = LoggerServer
    fields = ['name']


class SyslogLoggerServerCreateView(CreateView):

    model = SyslogLoggerServer
    fields = [
        'name', 'hostname', 'port', 'protocol', 'facility', 'default_log_level'
    ]


class SyslogLoggerServerDetailView(DetailView):

    model = SyslogLoggerServer
