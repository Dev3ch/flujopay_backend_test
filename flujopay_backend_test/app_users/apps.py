import contextlib

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AppUsersConfig(AppConfig):
    name = "flujopay_backend_test.app_users"
    verbose_name = _("App Users")

    def ready(self):
        with contextlib.suppress(ImportError):
            import flujopay_backend_test.app_users.signals  # noqa: F401
