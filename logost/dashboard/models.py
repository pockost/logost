from django.db import models
from django.urls import reverse


class ClientServer(models.Model):
    name = models.CharField(max_length=250)
    hostname = models.CharField(max_length=63, blank=True, null=True)
    ip = models.GenericIPAddressField(blank=True, null=True)
    logger_servers = models.ManyToManyField(
        'logger.LoggerServer',
        through='LoggerServerStatus',
        related_name='client_servers')

    def send_log(self, message):
        """
        Send a log to all active logger
        """
        for logger_server in self.logger_servers.filter(
                client_status__enabled=True):
            logger_server.send_message(message)

    def get_absolute_url(self):
        return reverse('client-server-detail', args=[self.pk])


class LoggerServerStatus(models.Model):
    """
    Intermediate table for enabling/disabling logger server
    linked to ClientServer
    """
    enabled = models.BooleanField(default=True)

    client_server = models.ForeignKey(
        'ClientServer', related_name='logger_status', on_delete=models.CASCADE)
    logger_server = models.ForeignKey(
        'logger.LoggerServer',
        related_name='client_status',
        on_delete=models.CASCADE)
