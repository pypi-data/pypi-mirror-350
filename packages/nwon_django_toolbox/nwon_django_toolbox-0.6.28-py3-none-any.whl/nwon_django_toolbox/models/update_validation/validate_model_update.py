import datetime
from nwon_baseline.pydantic import pydantic_model_to_dict
from typing import List, Union

from pydantic import BaseModel
import pytz
from django.db.models import Model
from django.db.models.fields.files import ImageFieldFile
from rest_framework.exceptions import ValidationError

from nwon_django_toolbox.typings import AllowedUpdate


def validate_model_update(
    old_model_instance: Model,
    updated_model_instance: Model,
    allowed_updates: Union[List[AllowedUpdate], None],
):
    """
    Checks an update model instance against an allowed set of fields and their values
    """

    if updated_model_instance._state.adding is True:
        return

    if allowed_updates is None:
        return

    fields = updated_model_instance._meta.get_fields()

    allowed_field_names = [update.field_name for update in allowed_updates]

    if old_model_instance.__class__ != updated_model_instance.__class__:
        raise ValidationError(
            f"You tried to validate update for two instances of a different class: "
            f"{old_model_instance.__class__}  and "
            f"{updated_model_instance.__class__}"
        )

    if old_model_instance.pk != updated_model_instance.pk:
        raise ValidationError(
            f"You tried to validate update for two instances of "
            f"{old_model_instance.__class__} with a different pk value: "
            f"{old_model_instance.pk} and {updated_model_instance.pk}"
        )

    for field in fields:
        field_name = field.name
        old_value = getattr(old_model_instance, field_name)
        new_value = getattr(updated_model_instance, field_name)

        if isinstance(old_value, ImageFieldFile) and isinstance(
            new_value, ImageFieldFile
        ):
            old_value = old_value.url if old_value else None
            new_value = new_value.url if new_value else None

        if isinstance(old_value, datetime.datetime) and old_value.tzinfo is None:
            old_value = pytz.utc.localize(old_value)

        if isinstance(new_value, datetime.datetime) and new_value.tzinfo is None:
            new_value = pytz.utc.localize(new_value)


        if isinstance(old_value, BaseModel):
            old_value = pydantic_model_to_dict(old_value)

        if isinstance(new_value, BaseModel):
            new_value = pydantic_model_to_dict(new_value)


        """
        When working with polymorphic models it was problematic to compare the full
        instances. Therefore we compare the pk values instead.

        If the model type is wrong the model itself will raise an error when saving.
        """
        if isinstance(old_value, Model):
            old_value = old_value.pk

        if isinstance(new_value, Model):
            new_value = new_value.pk

        if old_value == new_value:
            continue

        if field_name not in allowed_field_names:
            raise ValidationError(
                {
                    field_name: f"You are not allowed to update {field_name} "
                    f"with value {new_value} from {old_value} for "
                    f"{updated_model_instance.__class__} "
                    f"with pk {updated_model_instance.pk}"
                }
            )

        allowed_updates_for_field_name = _filter_allowed_updates(
            allowed_updates, field_name
        )

        # There is some configuration which limits possible field values
        new_value_has_constraint = any(
            x.allowed_values is not None for x in allowed_updates_for_field_name
        )

        # The new value is explicitly allowed in some field configuration
        new_value_matches_constraint = any(
            new_value in x.allowed_values
            for x in allowed_updates_for_field_name
            if x.allowed_values
        )

        if new_value and new_value_has_constraint and not new_value_matches_constraint:
            raise ValidationError(
                {
                    field_name: f"{new_value} can't be set as value for "
                    f"{field_name} in {updated_model_instance} with pk "
                    f"{updated_model_instance.pk}"
                }
            )


def _filter_allowed_updates(
    allowed_updates: List[AllowedUpdate], field_name: str
) -> List[AllowedUpdate]:
    return list(
        filter(
            lambda x: field_name == x.field_name and x.allowed_values,
            allowed_updates,
        )
    )
