from django.urls import path

from . import views

urlpatterns = [
    path(
        'regex/create',
        views.RegexGeneatorCreateView.as_view(),
        name='generator-regex-create'),
    path(
        'regex/<int:pk>',
        views.RegexGeneratorDetailView.as_view(),
        name='generator-regex-detail'),
    path(
        'regex/edit/<int:pk>',
        views.RegexGeneratorUpdateView.as_view(),
        name='generator-regex-edit'),
    path(
        'grok/create',
        views.GrokGeneatorCreateView.as_view(),
        name='generator-grok-create'),
    path(
        'grok/<int:pk>',
        views.GrokGeneratorDetailView.as_view(),
        name='generator-grok-detail'),
    path(
        'grok/edit/<int:pk>',
        views.GrokGeneratorUpdateView.as_view(),
        name='generator-grok-edit'),
    path(
        'httpd/create',
        views.ApacheHttpdGeneatorCreateView.as_view(),
        name='generator-httpd-create'),
    path(
        'httpd/<int:pk>',
        views.ApacheHttpdGeneratorDetailView.as_view(),
        name='generator-httpd-detail'),
    path(
        'httpd/edit/<int:pk>',
        views.ApacheHttpdGeneratorUpdateView.as_view(),
        name='generator-httpd-edit'),
    path(
        'delete/<int:pk>',
        views.GeneratorDeleteView.as_view(),
        name='generator-delete'),
    path(
        'generate/<int:pk>',
        views.GeneratorGenerateView.as_view(),
        name='generator-generate'),
    path('', views.GeneratorListView.as_view(), name='generator-list'),
]