from django import forms

from .models import ClientServer, GeneratorStatus, LoggerServerStatus


class ClientServerForm(forms.ModelForm):
    """
    A form object of ClientServer object
    The main goal is to handle to ability to save the m2m related field
    (logger_servers) through the LoggerServerStatus table
    Same for generators
    """

    def save(self, commit=True):
        obj = super().save(commit=False)
        if commit:
            obj.save()
            # Logger M2M
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

            # Geneator M2M
            if 'generators' in self.changed_data:
                final_generators = self.cleaned_data['generators'].all()
                initial_generators = self.initial[
                    'generators'] if 'generators' in self.initial else list()

                # create and save new members
                for generator in final_generators:
                    if generator not in initial_generators:
                        GeneratorStatus.objects.create(
                            client_server=obj, generator=generator)

                # delete old members that were removed from the form
                for generator in initial_generators:
                    if generator not in final_generators:
                        GeneratorStatus.objects.filter(
                            client_server=obj, generator=generator).delete()
        return obj

    class Meta:
        model = ClientServer
        fields = [
            'name', 'hostname', 'ip', 'logger_servers', 'generators',
            'recurrence'
        ]


class SendLogForm(forms.Form):
    message = forms.CharField()
