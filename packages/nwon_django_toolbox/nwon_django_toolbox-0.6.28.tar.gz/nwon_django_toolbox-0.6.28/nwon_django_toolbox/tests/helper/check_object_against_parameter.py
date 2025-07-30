import logging
from typing import Optional

from humps.main import decamelize
from nwon_baseline.typings import AnyDict

from nwon_django_toolbox.settings import NWON_DJANGO_SETTINGS

LOGGER = logging.getLogger(NWON_DJANGO_SETTINGS.logger_name)


def check_object_against_parameter(
    object_to_test: AnyDict,
    parameter: AnyDict,
    exclude_keys: Optional[list[str]] = None,
):
    if exclude_keys is None:
        exclude_keys = []

    for key in parameter:
        """
        Skip parameters. This might make sense for parameters that do not get
        returned like some of the polymorphic models
        """
        if (
            NWON_DJANGO_SETTINGS.tests
            and key in NWON_DJANGO_SETTINGS.tests.keys_to_skip_on_api_test
        ):
            continue

        if key in exclude_keys:
            continue

        parameter_value = None
        if key in parameter and isinstance(parameter[key], dict):
            parameter_value = decamelize(parameter[key]).__str__()

        target_value = None
        if key in object_to_test and isinstance(object_to_test[key], dict):
            target_value = decamelize(object_to_test[key]).__str__()

        if target_value != parameter_value:
            LOGGER.debug(
                "Key "
                + key
                + " differs, \nParameter: \n"
                + parameter_value
                + " \n\nObject to test: \n"
                + target_value
            )

        assert parameter_value == target_value


__all__ = ["check_object_against_parameter"]
