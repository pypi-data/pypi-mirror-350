from typing import List, Optional

from django.db.models import Model

from nwon_django_toolbox.typings import AllowedUpdate


def allow_updates_for_model(
    model_instance: Model, disallowed_field_names: Optional[List[str]] = None
) -> List[AllowedUpdate]:
    """
    Returns an AllowedUpdate array which allows updating all fields except
    for the ones given by argument
    """

    fields = model_instance._meta.get_fields()
    return [
        AllowedUpdate(
            field_name=field.name,
        )
        for field in fields
        if disallowed_field_names is None or field.name not in disallowed_field_names
    ]
