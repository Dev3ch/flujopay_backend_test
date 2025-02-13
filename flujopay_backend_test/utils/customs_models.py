from django.db import models
from model_utils.models import TimeStampedModel
from simple_history.models import HistoricalRecords


class CustomModel(TimeStampedModel):
    is_active = models.BooleanField(verbose_name="¿Activo?", default=True)

    history = HistoricalRecords(inherit=True)

    class Meta:
        abstract = True
