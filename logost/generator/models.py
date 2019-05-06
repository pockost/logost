import exrex
from django.db import models
from django.urls import reverse
from polymorphic.models import PolymorphicModel

from .utils import convert_grok_to_regex

IP_REGEX = '\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'
APACHE_START = '\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b - - \[(0[1-9]|[12][0-9]|3[01])/(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)/(19|20)\d\d:(0[1-9]|[1][0-9]|2[03]):[0-5]\d:[0-5]\d \+0[0-9]00\]'


class Generator(PolymorphicModel):
    """
    A Generator is responsive of generating dummy log
    This is the base class
    """
    _type = ''
    name = models.CharField(max_length=255)

    @property
    def type(self):
        return self._type

    def generate(self):
        """
        This function should retourn a new generated log message
        """
        raise NotImplementedError(
            'generate method should be override on Generator child')

    def __str__(self):
        return self.name


class RegexGenerator(Generator):
    """
    A Generator based on regex
    """

    _type = 'regex'
    regex = models.CharField(max_length=10000)

    def generate(self):
        """
        Return a generated log based on regex
        """
        return exrex.getone(self.regex)

    def get_absolute_url(self):
        return reverse('generator-regex-detail', args=[self.pk])


class GrokGenerator(RegexGenerator):
    """
    A grok based generator.
    A Grok is a named regex. This generator can combine many grok
    in order to be mre readable.

    For performance purpose when the grok list is saved a new regex
    is generated and saved as RegexGenerator.
    """

    _type = 'grok'
    grok = models.CharField(max_length=10000)

    def save(self, *args, **kwargs):
        """
        When saving a grok partern we will expend the grok
        in order to generate a regex
        """
        self.regex = convert_grok_to_regex(self.grok)

        super(GrokGenerator, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('generator-grok-detail', args=[self.pk])


class ApacheHttpdGenerator(GrokGenerator):
    """
    An apache2 HTTPd generator
    """

    _type = 'httpd'

    def save(self, *args, **kwargs):
        """
        When saving we will trigger grok save in order to
        save the resulting regex. This is a performance tips
        """
        self.grok = '%{IP4} - - \[%{DAY}/%{MONTH_SHORT}/%{YEAR}:%{HOUR}:%{MINUTE}:%{SECOND} %{ISO8601_TIMEZONE}\] "%{HTTP_VERB} /nOdDNb8z8rs %{HTTP_PROTO}" (200|404|403|500) \d{3,6}'
        super(ApacheHttpdGenerator, self).save(*args, **kwargs)
