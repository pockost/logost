from django import forms

from .models import ClientServer, LoggerServerStatus


class ClientServerForm(forms.ModelForm):
    """
    A form object of ClientServer object
    The main goal is to handle to ability to save the m2m related field
    (logger_servers) through the LoggerServerStatus table
    """

    def save(self, commit=True):
        obj = super().save(commit=False)
        if commit:
            obj.save()
            if 'logger_servers' in self.changed_data:
                final_logger_servers = self.cleaned_data['logger_servers'].all(
                )
                initial_logger_servers = self.initial[
                    'logger_servers'] if 'logger_servers' in self.initial else list(
                    )

                # create and save new members
                for logger_server in final_logger_servers:
                    if logger_server not in initial_logger_servers:
                        LoggerServerStatus.objects.create(
                            client_server=obj, logger_server=logger_server)

                # delete old members that were removed from the form
                for logger_server in initial_logger_servers:
                    if logger_server not in final_logger_servers:
                        LoggerServerStatus.objects.filter(
                            client_server=obj,
                            logger_server=logger_server).delete()

        return obj

    class Meta:
        model = ClientServer
        fields = ['name', 'hostname', 'ip', 'logger_servers']


class SendLogForm(forms.Form):
    message = forms.CharField()
