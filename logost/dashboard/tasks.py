from datetime import timedelta

from celery.decorators import periodic_task
from django.db.models import F, Q
from django.utils import timezone

from .models import ClientServer


@periodic_task(run_every=timedelta(seconds=1))
def send_log():

    # TODO get panic
    # Get all ClientServer needing to send log
    clients = ClientServer.objects.filter(
        last_run__lt=(timezone.now() - F('recurrence')))

    for client in clients.iterator():
        client.periodic_send_log()

    return clients
