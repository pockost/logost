from django.db import models


class ClientServer(models.Model):
    name = models.CharField(max_length=250)
    hostname = models.CharField(max_length=63, blank=True, null=True)
    ip = models.GenericIPAddressField(blank=True, null=True)
    logger_servers = models.ManyToManyField(
        'logger.LoggerServer',
        through='LoggerServerStatus',
        related_name='client_servers')


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
