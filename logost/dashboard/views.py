from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from .forms import ClientServerForm, SendLogForm
from .models import ClientServer


class ClientServerListView(ListView):

    model = ClientServer
    paginate_by = 100


class ClientServerDetailView(DetailView):

    model = ClientServer


class ClientServerCreateView(CreateView):

    model = ClientServer
    form_class = ClientServerForm


class ClientServerUpdateView(UpdateView):
    model = ClientServer
    form_class = ClientServerForm


class ClientServerDeleteView(DeleteView):
    model = ClientServer
    success_url = reverse_lazy('client-server-list')


class ClientServerSendLogView(SingleObjectMixin, FormView):
    template_name = 'dashboard/clientserver_form.html'
    form_class = SendLogForm
    model = ClientServer
    object = None

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.send_log("toto")
        messages.success(request, 'Log successfully placed to be send.')
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy(
            'client-server-detail', kwargs={'pk': self.object.pk})
