import datetime

from django.db import models
from django.urls import reverse
from django.utils import timezone


class ClientServer(models.Model):
    name = models.CharField(max_length=250)
    hostname = models.CharField(max_length=63, blank=True, null=True)
    ip = models.GenericIPAddressField(blank=True, null=True)
    logger_servers = models.ManyToManyField(
        'logger.LoggerServer',
        through='LoggerServerStatus',
        related_name='client_servers')
    generators = models.ManyToManyField(
        'generator.Generator',
        through='GeneratorStatus',
        related_name='client_servers')
    recurrence = models.DurationField(default=datetime.timedelta(seconds=5))
    last_run = models.DateTimeField(default=timezone.now)

    def periodic_send_log(self):
        """
        Get a log from all generator and send to all logger
        """
        for generator in self.generators.filter(client_status__enabled=True):
            message = generator.generate()
            # If message is a list all should be send in setted order
            # This can be usefull for the instance for ssh generator
            if type(message) == list:
                for m in message:
                    self.send_log(m)
            else:
                self.send_log(message)
        self.last_run = timezone.now()
        self.save()

    def send_log(self, message):
        """
        Send a log to all active logger
        """
        for logger_server in self.logger_servers.filter(
                client_status__enabled=True):
            logger_server.send_message(message, self)

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


class GeneratorStatus(models.Model):
    """
    Intermediate table for enabling/disabling generator
    linked to ClientServer
    """
    enabled = models.BooleanField(default=True)

    client_server = models.ForeignKey(
        'ClientServer',
        related_name='generator_status',
        on_delete=models.CASCADE)
    generator = models.ForeignKey(
        'generator.Generator',
        related_name='client_status',
        on_delete=models.CASCADE)
