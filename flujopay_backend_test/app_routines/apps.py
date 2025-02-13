import contextlib

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AppRoutinesConfig(AppConfig):
    name = "flujopay_backend_test.app_routines"
    verbose_name = _("App Users")

    def ready(self):
        with contextlib.suppress(ImportError):
            import flujopay_backend_test.app_routines.signals  # noqa: F401
