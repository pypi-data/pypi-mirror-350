import logging
from typing import Optional, Type

from django.db.models import Model
from humps.main import decamelize
from nwon_baseline.typings import AnyDict
from rest_framework.serializers import Serializer

from nwon_django_toolbox.settings import NWON_DJANGO_SETTINGS

LOGGER = logging.getLogger(NWON_DJANGO_SETTINGS.logger_name)


def dictionary_is_serialized_instance(
    instance: Model,
    serializer: Type[Serializer],
    response: AnyDict,
    decamelize_response: bool = True,
    exclude_keys: Optional[list[str]] = None,
) -> bool:
    """
    Checks that a dictionary resembles the serialization of a model instance
    with a certain serializer.
    """

    """
    We need to decamelize the dict as well in case there is some nested data in it that
    has camel case keys.
    """
    serialized_dict = serializer(instance=instance).data
    serialized_dict = (
        decamelize(serialized_dict) if decamelize_response else serialized_dict
    )

    compare_dict = decamelize(response) if decamelize_response else response

    if exclude_keys:
        for key in exclude_keys:
            compare_dict.pop(key, None)
            serialized_dict.pop(key, None)

    is_equal = serialized_dict == compare_dict

    if not is_equal:
        difference = {
            k: compare_dict[k] for k in set(compare_dict) - set(serialized_dict)
        }
        LOGGER.debug(
            f"Dictionary differs from serialized data from {serializer.__name__}: \n {difference}"
        )

    return is_equal


__all__ = ["dictionary_is_serialized_instance"]
