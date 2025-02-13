from typing import ClassVar

from django.contrib.auth.models import AbstractUser
from django.db import models

from flujopay_backend_test.utils.customs_models import CustomModel

from .managers import UserManager


class User(AbstractUser, CustomModel):
    username = None
    first_name = None
    last_name = None
    names = models.CharField(verbose_name="Nombres", max_length=100, blank=True)
    surnames = models.CharField(verbose_name="Apellidos", max_length=100, blank=True)
    email = models.EmailField(verbose_name="Correo", unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects: ClassVar[UserManager] = UserManager()

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return self.email
