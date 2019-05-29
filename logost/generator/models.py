import datetime
import random
import re

import exrex
import pytz
from django.db import models
from django.urls import reverse
from polymorphic.models import PolymorphicModel

from . import grok
from .utils import convert_grok_to_regex


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

    random_date = models.BooleanField(default=True)
    only_get_post_verb = models.BooleanField(default=False)
    custom_url = models.CharField(blank=True, default='', max_length=400)
    only_http_11 = models.BooleanField(default=True)

    def generate(self):
        """
        Generate a log
        Call parent for regex handling.
        If random_date is false set current date
        """
        message = super(ApacheHttpdGenerator, self).generate()
        if not self.random_date:
            current_date = datetime.datetime.now(
                pytz.utc).strftime('%d/%b/%Y:%H:%M:%S %z')
            message = re.sub(r'###DATE###', current_date, message)
        return message

    def save(self, *args, **kwargs):
        """
        When saving we will trigger grok save in order to
        save the resulting regex. This is a performance tips
        """
        grok = '%{IP4} - - '

        # Manage options

        # Date
        if not self.random_date:
            grok += '\[###DATE###\]'
        else:
            grok += '\[%{DAY}/%{MONTH_SHORT}/%{YEAR}:%{HOUR}:%{MINUTE}:%{SECOND} %{ISO8601_TIMEZONE}\]'

        grok += ' '

        # HTTP Verb
        if self.only_get_post_verb:
            grok += '%{HTTP_VERB_GETPOST}'
        else:
            grok += '%{HTTP_VERB}'

        grok += ' '

        # URL
        if self.custom_url != '':
            grok += self.custom_url
        else:
            grok += '/(%{WORD}/)+'
        grok += ' '

        # HTTP Protocol
        if self.only_http_11:
            grok += 'HTTP/1\.1'
        else:
            grok += '%{HTTP_PROTO}'
        grok += '" '

        grok += '(200|404|403|500) \d{3,6}'

        self.grok = grok
        super(ApacheHttpdGenerator, self).save(*args, **kwargs)


class VsftpdGenerator(GrokGenerator):
    """
    A vsftpd generator
    """

    _type = 'vsftpd'

    custom_url = models.CharField(blank=True, default='', max_length=400)
    custom_username = models.CharField(blank=True, default='', max_length=400)
    random_date = models.BooleanField(default=True)

    def generate(self):
        """
        Generate a log
        Call parent for regex handling.
        If random_date is false set current date
        """
        message = super(VsftpdGenerator, self).generate()
        if not self.random_date:
            current_date = datetime.datetime.now(
                pytz.utc).strftime('%d/%b/%Y:%H:%M:%S %z')
            message = re.sub(r'###DATE###', current_date, message)
        return message

    def save(self, *args, **kwargs):
        """
        When saving we will trigger grok save in order to
        save the resulting regex. This is a performance tips
        """
        grok = ''

        # Manage options

        # Date
        if not self.random_date:
            grok += '###DATE###'
        else:
            grok += '%{DAY_SHORT} %{MONTH_SHORT} %{DAY} %{HOUR}:%{MINUTE}:%{SECOND} %{YEAR}'

        grok += ' '

        # Transfert time
        # The total time of the transfer in seconds.
        grok += '\d{1,2}'
        grok += ' '

        # remote-host
        # The remote host name
        grok += '%{IP4}'
        grok += ' '

        # byte-count
        # The amount of transferred bytes
        grok += '\d{4,6}'
        grok += ' '

        # filename
        # The canonicalized (all symbolic links are resolved) abso-lute pathname of the transferred file.
        if self.custom_url != '':
            grok += self.custom_url
        else:
            grok += '/(%{WORD}/)+'
        grok += ' '

        # transfer-type
        # The single character that indicates the type of the trans-fer. The set of possible values is:
        #   a         An ascii transfer.
        #   b         A binary transfer.
        grok += '(a|b)'
        grok += ' '

        # special-action-flag
        # One or more single character flags indicating any special action taken. The set of possible values is:
        # _          No action was taken
        # C         The file was compressed (not in use).
        # U         The file was uncompressed (not in use).
        # T         The file was tar'ed (not in use).
        grok += '_'
        grok += ' '

        # direction
        # The direction of the transfer. The set of possible values is:
        # o          The outgoing transfer.
        # i           The incoming transfer.
        grok += '(o|i)'
        grok += ' '

        # access-mode
        # The method by which the user is logged in. The set of pos-sible values is:
        # a (anonymous)  The anonymous guest user.
        # g (guest)           The real but chrooted user (this capability is guided by ftpchroot(5) file).
        # r (real)           The real user.
        grok += 'g'
        grok += ' '

        # username
        # The user's login name in case of the real user, or the user's identification string in case of the anonymous
        # user (by convention it is an email address of the user).
        if self.custom_username != '':
            grok += self.custom_username
        else:
            grok += '%{USERNAME}'
        grok += ' '

        # service-name
        # The name of the service being invoked. The ftpd( utility uses the ``ftp'' keyword.
        grok += 'ftp'
        grok += ' '

        # authentication-method
        # The used method of the authentication. The set of possible values is:
        # 0         None.
        # 1         RFC931 Authentication (not in use).
        grok += '0'
        grok += ' '

        # authenticated-user-id
        # The user id returned by the authentication method. The `*' symbol is used if an authenticated user id is not
        # avail-able.
        grok += '*'
        grok += ' '

        # completion-status
        # The single character that indicates the status of the transfer. The set of possible values is:
        # c         A complete transfer.
        # i         An incomplete transfer.
        grok += 'c|i'
        grok += ' '

        self.grok = grok
        super(VsftpdGenerator, self).save(*args, **kwargs)


class SshdGenerator(GrokGenerator):
    """
    An sshd log generator

    This generator will produce log like that

    For error
    May 29 13:22:36 server1 sshd[446]: Invalid user tajiki from 137.74.129.189 port 48102
    May 29 13:22:36 server1 sshd[446]: input_userauth_request: invalid user tajiki [preauth]
    May 29 13:22:36 server1 sshd[446]: pam_unix(sshd:auth): check pass; user unknown
    May 29 13:22:36 server1 sshd[446]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=137.74.129.189
    May 29 13:22:38 server1 sshd[446]: Failed password for invalid user tajiki from 137.74.129.189 port 48102 ssh2
    May 29 13:22:38 server1 sshd[446]: Received disconnect from 137.74.129.189 port 48102:11: Bye Bye [preauth]
    May 29 13:22:38 server1 sshd[446]: Disconnected from 137.74.129.189 port 48102 [preauth]

    For correct connection
    May 29 13:30:08 server1 sshd[3850]: Accepted publickey for myuser from XXX.XXX.XXX.XXX port 36746ssh2: RSA SHA256:XXXXXXXXXXXXXXXXXXXXX
    May 29 13:30:08 server1 sshd[3850]: pam_unix(sshd:session): session opened for user myuser by (uid=0)
    May 29 13:35:24 pockost-docker0 sshd[6232]: Received disconnect from XXX.XXX.XXX.XXX port 37566:11: disconnected by user
    May 29 13:35:24 pockost-docker0 sshd[6232]: Disconnected from XXX.XXX.XXX.XXX port 37566
    May 29 13:35:24 pockost-docker0 sshd[6226]: pam_unix(sshd:session): session closed for user myuser
    """

    _type = 'sshd'
    _date_grok = '%{MONTH_SHORT} %{DAY} %{HOUR}:%{MINUTE}:%{SECOND}'

    # TODO
    # username_list
    # source ip list
    # Only error

    def generate(self):
        """
        Generate many log
        """
        # Get a random IP address for remote host
        ip = exrex.getone(convert_grok_to_regex(grok.IP4))
        # Get a random username for connexion
        username = exrex.getone(convert_grok_to_regex(grok.USERNAME))
        # Get a random port
        port = exrex.getone(convert_grok_to_regex(grok.PORT))
        # Get a random date
        date = exrex.getone(convert_grok_to_regex(self._date_grok))
        # Get a pid
        pid = exrex.getone(convert_grok_to_regex(grok.PORT))
        # get server hostname
        hostname = 'server1'

        is_error = bool(random.getrandbits(1))

        if is_error:
            return self.generate_error(ip, username, port, date, pid, hostname)
        return self.generate_success(ip, username, port, date, pid, hostname)

    def generate_error(self, ip, username, port, date, pid, hostname):
        """
        Generate an ordered list of grok for ssh errored login
        """
        logs = list()

        # May 29 13:22:36 server1 sshd[446]: Invalid user tajiki from 137.74.129.189 port 48102
        logs.append(
            '{date} {hostname} sshd[{pid}]: Invalid user {username} from {ip} port {port}'
            .format(
                date=date,
                hostname=hostname,
                pid=pid,
                username=username,
                ip=ip,
                port=port))

        #  May 29 13:22:36 server1 sshd[446]: input_userauth_request: invalid user tajiki [preauth]
        logs.append(
            '{date} {hostname} sshd[{pid}]: input_userauth_request: invalid user {username} [preauth]'
            .format(date=date, hostname=hostname, username=username, pid=pid))

        # May 29 13:22:36 server1 sshd[446]: pam_unix(sshd:auth): check pass; user unknown
        logs.append(
            '{date} {hostname} sshd[{pid}]: pam_unix(sshd:auth): check pass; user unknown'
            .format(date=date, hostname=hostname, pid=pid))

        # May 29 13:22:36 server1 sshd[446]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=137.74.129.189
        logs.append(
            '{date} {hostname} sshd[{pid}]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost={ip}'
            .format(date=date, hostname=hostname, pid=pid, ip=ip))

        # May 29 13:22:38 server1 sshd[446]: Failed password for invalid user tajiki from 137.74.129.189 port 48102 ssh2
        logs.append(
            '{date} {hostname} sshd[{pid}]: Failed password for invalid user {username} from {ip} port {port} ssh2'
            .format(
                date=date,
                hostname=hostname,
                pid=pid,
                username=username,
                port=port,
                ip=ip))

        # May 29 13:22:38 server1 sshd[446]: Received disconnect from 137.74.129.189 port 48102:11: Bye Bye [preauth]
        logs.append(
            '{date} {hostname} sshd[{pid}]: Received disconnect from {ip} port {port}:11: Bye Bye [preauth]'
            .format(date=date, hostname=hostname, pid=pid, port=port, ip=ip))

        # May 29 13:22:38 server1 sshd[446]: Disconnected from 137.74.129.189 port 48102 [preauth]
        logs.append(
            '{date} {hostname} sshd[{pid}]: Disconnected from {ip} port {port} [preauth]'
            .format(date=date, hostname=hostname, pid=pid, port=port, ip=ip))

        return logs

    def generate_success(self, ip, username, port, date, pid, hostname):
        """
        Generate an ordered list of grok for succesfull ssh login
        """
        logs = list()
        rsa = exrex.getone('[0-9a-zA-Z+=]{40,50}')

        # May 29 13:30:08 server1 sshd[3850]: Accepted publickey for myuser from XXX.XXX.XXX.XXX port 36746 ssh2: RSA SHA256:XXXXX
        logs.append(
            '{date} {hostname} sshd[{pid}]: Accepted publickey for {username} from {ip} port {port} ssh2: RSA SHA256:{rsa}'
            .format(
                date=date,
                hostname=hostname,
                pid=pid,
                port=port,
                ip=ip,
                rsa=rsa,
                username=username))

        # May 29 13:30:08 server1 sshd[3850]: pam_unix(sshd:session): session opened for user myuser by (uid=0)
        logs.append(
            '{date} {hostname} sshd[{pid}]: pam_unix(sshd:session): session opened for user {username} by (uid=0)'
            .format(date=date, hostname=hostname, pid=pid, username=username))

        # May 29 13:35:24 pockost-docker0 sshd[6232]: Received disconnect from XXX.XXX.XXX.XXX port 37566:11: disconnected by user
        logs.append(
            '{date} {hostname} sshd[{pid}]: Received disconnect from {ip} port {port}:11: disconnected by user'
            .format(date=date, hostname=hostname, pid=pid, ip=ip, port=port))

        # May 29 13:35:24 pockost-docker0 sshd[6232]: Disconnected from XXX.XXX.XXX.XXX port 37566
        logs.append(
            '{date} {hostname} sshd[{pid}]: Disconnected from {ip} port {port}'
            .format(date=date, hostname=hostname, pid=pid, ip=ip, port=port))

        # May 29 13:35:24 pockost-docker0 sshd[6226]: pam_unix(sshd:session): session closed for user myuser
        logs.append(
            '{date} {hostname} sshd[{pid}]: pam_unix(sshd:session): session closed for user {username}'
            .format(date=date, hostname=hostname, pid=pid, username=username))

        return logs
