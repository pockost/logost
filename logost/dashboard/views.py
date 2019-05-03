from django.views.generic.list import ListView

from .models import ClientServer


class ClientServerListView(ListView):

    model = ClientServer
    paginate_by = 100
