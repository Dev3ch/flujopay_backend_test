from typing import Any

from django.db.models import Manager
from django.utils.timezone import now
from rest_framework import serializers

from flujopay_backend_test.utils.customs_errors import InternalServerError
from flujopay_backend_test.utils.logging_error import custom_logger
from flujopay_backend_test.utils.simple_functions import convert_to_primary_key
from flujopay_backend_test.utils.simple_functions import generate_instance_ids


class CRUMixinSerializer:
    def set_allow_blank(self, allow_blank: bool):  # noqa: FBT001
        for field_name in self.Meta.fields:
            field = self.fields.get(field_name)

            if hasattr(field, "allow_blank"):
                field.allow_blank = allow_blank

    def handle_nested_data(
        self,
        nested_data: list[dict],
        serializer_class: Any,
        field: str,
        parent_instance=None,
    ):
        for data in nested_data:
            instance = data.get("id", None)
            data[field] = parent_instance
            data = convert_to_primary_key(data)  # noqa: PLW2901

            if instance:
                serializer = serializer_class(
                    instance=instance,
                    data=data,
                    context=self.context,
                    partial=True,
                )

            else:
                serializer = serializer_class(data=data, context=self.context)

            serializer.is_valid(raise_exception=True)
            serializer.save()

    def handle_nested_data_with_should_delete(
        self,
        nested_data: list[dict],
        serializer_class: Any,
        field: str,
        parent_instance: Any,
        attribute_name: str,
    ):
        items_with_should_delete_set_to_true = (
            self.filter_items_with_should_delete_set_to_true(nested_data)
        )
        items_ids = generate_instance_ids(items_with_should_delete_set_to_true)
        related_set = getattr(parent_instance, attribute_name)
        related_set.remove_the_filter_from_a_list_of_ids(items_ids)
        items_with_should_delete_set_to_false = (
            self.filter_items_with_should_delete_set_to_false(nested_data)
        )

        self.handle_nested_data(
            items_with_should_delete_set_to_false,
            serializer_class,
            field,
            parent_instance,
        )

    def excluded_fields(self):
        return []

    def _validate(self, attrs: dict, error_key: str | None = None) -> dict:
        try:
            validation_methods = [
                method_name
                for method_name in dir(self)
                if method_name.startswith("_validate_")
            ]
            for method_name in validation_methods:
                method = getattr(self, method_name)
                method(attrs)

        except ValueError as error:
            error_dict = (
                error.args[0] if isinstance(error.args[0], dict) else {str(error)}
            )

            if error_key:
                error_dict = {error_key: [error_dict]}

            raise serializers.ValidationError(error_dict) from error

        except (KeyError, AttributeError, TypeError) as error:
            self.send_error_to_contact_support(error)

    def update_fields(
        self,
        instance: Any,
        validated_data: dict,
        excluded_fields: list[str],
    ):
        initial_data = validated_data.copy()

        excluded_fields = [*excluded_fields, "id"]
        for key, value in initial_data.items():
            if key in excluded_fields:
                continue

            setattr(instance, key, value)

        instance.last_updated = now()

    def generate_initial_data(self, validated_data: dict, excluded_fields: list[str]):
        initial_data = validated_data.copy()

        for key in validated_data:
            if key in excluded_fields:
                initial_data.pop(key, None)

        return initial_data

    def filter_items_with_should_delete_set_to_true(self, items: list[dict]):
        return [item for item in items if item.get("should_delete", False)]

    def filter_items_with_should_delete_set_to_false(self, items: list[dict]):
        return [item for item in items if not item.get("should_delete", False)]

    def throw_mandatory_field_error(self, field: Any, error_key: str):
        if field in [None, "", []]:
            raise ValueError(
                {error_key: ["Campo requerido, no puede ser null ni vacío"]},
            )

    def send_error_to_contact_support(self, error: Exception | None = None):
        logger = custom_logger()
        logger.error(f"Error: {error}", exc_info=True)  # noqa: G004

        raise InternalServerError(
            {"errors": ["Algo salió mal, contáctate con el soporte de la web"]},
        )

    def get_value_from_attrs(self, field: str) -> Any:
        attrs = self.context["attrs"] or {}

        instance_value = getattr(self.instance, field) if self.instance else None
        if isinstance(instance_value, Manager):
            instance_value = instance_value.all()

        return attrs.get(field, instance_value)


class BaseSerializer(CRUMixinSerializer, serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.fields.get("id", None) is not None:
            is_new_instance = self.instance is None
            self.fields["id"].required = not is_new_instance

    def is_valid(self, raise_exception=False):  # noqa: FBT002
        valid = super().is_valid(raise_exception=raise_exception)

        attrs = self.validated_data.copy()
        self.context["attrs"] = attrs

        self._validate(attrs)

        return valid


class ModelBaseSerializer(CRUMixinSerializer, serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        is_new_instance = self.instance is None
        self.fields["id"].required = not is_new_instance

    def is_valid(self, raise_exception=False):  # noqa: FBT002
        valid = super().is_valid(raise_exception=raise_exception)

        attrs = self.validated_data.copy()
        self.context["attrs"] = attrs

        self._validate(attrs)

        return valid
