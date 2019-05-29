from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from .models import ApacheHttpdGenerator, Generator, GrokGenerator, RegexGenerator, SshdGenerator, VsftpdGenerator


class GeneratorListView(ListView):

    model = Generator


class RegexGeneratorUpdateView(UpdateView):

    model = RegexGenerator
    fields = ['name', 'regex']


class RegexGeneatorCreateView(CreateView):

    model = RegexGenerator
    fields = ['name', 'regex']


class RegexGeneratorDetailView(DetailView):

    model = RegexGenerator


class GeneratorDeleteView(DeleteView):

    model = Generator
    success_url = reverse_lazy('generator-list')


class GrokGeneratorUpdateView(UpdateView):

    model = GrokGenerator
    fields = ['name', 'grok']


class GrokGeneatorCreateView(CreateView):

    model = GrokGenerator
    fields = ['name', 'grok']


class GrokGeneratorDetailView(DetailView):

    model = GrokGenerator


class ApacheHttpdGeneratorUpdateView(UpdateView):

    model = ApacheHttpdGenerator
    fields = [
        'name', 'random_date', 'only_get_post_verb', 'custom_url',
        'only_http_11'
    ]


class ApacheHttpdGeneatorCreateView(CreateView):

    model = ApacheHttpdGenerator
    fields = [
        'name', 'random_date', 'only_get_post_verb', 'custom_url',
        'only_http_11'
    ]


class ApacheHttpdGeneratorDetailView(DetailView):

    model = ApacheHttpdGenerator


class VsftpdGeneratorUpdateView(UpdateView):

    model = VsftpdGenerator
    fields = ['name', 'random_date', 'custom_url', 'custom_username']


class VsftpdGeneatorCreateView(CreateView):

    model = VsftpdGenerator
    fields = ['name', 'random_date', 'custom_url', 'custom_username']


class VsftpdGeneratorDetailView(DetailView):

    model = VsftpdGenerator


class SshdGeneratorUpdateView(UpdateView):

    model = SshdGenerator
    fields = ['name']


class SshdGeneatorCreateView(CreateView):

    model = SshdGenerator
    fields = ['name']


class SshdGeneratorDetailView(DetailView):

    model = SshdGenerator


class GeneratorGenerateView(SingleObjectMixin, TemplateView):
    template_name = 'generator/generator_generate.html'
    model = Generator
    object = None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        logs = self.object.generate()

        # We should return a list
        if isinstance(logs, str):
            logs = [logs]
        context['generated_log'] = logs

        return context
