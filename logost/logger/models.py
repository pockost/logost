import socket

from django.db import models
from django.urls import reverse
from polymorphic.models import PolymorphicModel

from . import flags


class LoggerServer(PolymorphicModel):
    """
    LoggerServer class is the base class for all logger.
    All logger type like syslog have to inherite from this class.
    For the instance we should have a class SyslogLoggerServer(LoggerServer)
    """
    name = models.CharField(max_length=255)

    def send_message(self, message, log_level=None):
        """
        This function should be implemented on child
        """
        raise NotImplementedError(
            'Send message should be override on LoggerServer child')


class SyslogLoggerServer(LoggerServer):
    """
    Syslog logger server
    """
    FACILITY_CHOICES = (
        (0, 'kern'),
        (1, 'user'),
        (2, 'mail'),
        (3, 'daemon'),
        (4, 'auth'),
        (5, 'syslog'),
        (6, 'lpr'),
        (7, 'news'),
        (8, 'uucp'),
        (9, 'cron'),
        (10, 'authpriv'),
        (11, 'ftp'),
        (12, 'ntp'),
        (13, 'security'),
        (14, 'console'),
        (15, 'solaris-cron'),
        (16, 'local0'),
        (17, 'local1'),
        (18, 'local2'),
        (19, 'local3'),
        (20, 'local4'),
        (21, 'local5'),
        (22, 'local6'),
        (23, 'local7'),
    )
    LOGLEVEL_CHOICES = (
        (0, 'emerg'),
        (1, 'alert'),
        (2, 'crit'),
        (3, 'err'),
        (4, 'warning'),
        (5, 'notice'),
        (6, 'info'),
        (7, 'debug'),
    )
    PROTOCOL_CHOICES = (
        (flags.TCP, 'TCP'),
        (flags.UDP, 'UDP'),
    )

    hostname = models.CharField(max_length=255)
    port = models.IntegerField()
    protocol = models.IntegerField(choices=PROTOCOL_CHOICES, default=flags.TCP)
    facility = models.IntegerField(choices=FACILITY_CHOICES, default=16)
    default_log_level = models.IntegerField(
        choices=LOGLEVEL_CHOICES, default=5)

    _connection = None

    def _get_connection(self):
        """
        Return a working connection to syslog server
        """
        if self._connection is None:
            if self.protocol == flags.TCP:
                self._connection = socket.socket(socket.AF_INET,
                                                 socket.SOCK_STREAM)
                self._tcp_connect()
            else:
                self._connection = socket.socket(socket.AF_INET,
                                                 socket.SOCK_DGRAM)
        return self._connection

    def _tcp_connect(self):
        """
        (re)Open TCP connection
        """
        if self.protocol == flags.TCP:
            self._connection.connect((self.hostname, self.port))

    def _construct_message(self, message, log_level):
        """
        Return a formated message to send to syslog server
        """
        return "<{level}>{message}\n".format(
            level=(log_level + self.facility * 8), message=message).encode()

    def send_message(self, message, log_level=None):
        """
        send message to syslog server
        """
        syslog_message = self._construct_message(
            message,
            log_level if log_level is not None else self.default_log_level)

        connection = self._get_connection()
        if self.protocol == flags.TCP:
            connection.send(syslog_message)
        else:
            connection.sendto(syslog_message, (self.hostname, self.port))

    def get_absolute_url(self):
        return reverse('logger-server-syslog-detail', args=[self.pk])
