from django.apps import AppConfig


class FminvoiceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'FMInvoice'

    def ready(self):
        import FMInvoice.signals  # Importer les signaux
