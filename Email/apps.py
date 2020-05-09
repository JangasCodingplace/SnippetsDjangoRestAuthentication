from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class EmailConfig(AppConfig):
    name = 'Email'
    verbose_name = _('Email')

    def ready(self):
        import Email.signals
