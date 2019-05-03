from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from .models import LoggerServer, SyslogLoggerServer


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
