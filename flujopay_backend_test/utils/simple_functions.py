from django.db import models
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken


def convert_to_primary_key(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if hasattr(value, "pk"):
                data[key] = value.pk
            else:
                data[key] = convert_to_primary_key(value)

    elif isinstance(data, list):
        data = [convert_to_primary_key(item) for item in data]

    elif isinstance(data, models.Model):
        data = data.pk

    return data


def generate_instance_ids(list_of_instances: list):
    list_of_instances_ids = []
    for instance in list_of_instances:
        try:
            list_of_instances_ids.append(
                instance["id"].pk if instance["id"] is not None else None,
            )

        except (KeyError, AttributeError, TypeError):
            list_of_instances_ids.append(None)

    return list_of_instances_ids


def get_tokens_jwt(user, lifetime_access: float, lifetime_refresh: float) -> dict:
    refresh: RefreshToken = RefreshToken.for_user(user)
    refresh.access_token_class.lifetime = timezone.timedelta(days=lifetime_access)
    refresh.set_exp(lifetime=timezone.timedelta(days=lifetime_refresh))
    return {"refresh": str(refresh), "access": str(refresh.access_token)}
