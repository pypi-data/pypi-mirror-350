from typing import Any, List, Optional, Type

from django.db.models.base import Model
from rest_framework.serializers import Serializer

from nwon_django_toolbox.tests.api_client.api_test import ApiTest
from nwon_django_toolbox.tests.helper.check_object_against_parameter import (
    check_object_against_parameter,
)
from nwon_django_toolbox.tests.helper.dictionary_is_serialized_instance import (
    dictionary_is_serialized_instance,
)
from nwon_django_toolbox.typings import RequestBodyFormat
from nwon_django_toolbox.url_helper import detail_url_for_model, list_url_for_model


def check_put_basics(
    model: Model,
    authentication_token: Optional[str] = None,
    needs_authentication: bool = True,
):
    """
    Test basics on a put endpoint.

    1. Unauthorized response without authentication and needs_authentication == True
    2. Not found on missing id
    3. Method not allowed on list url
    """

    list_url = list_url_for_model(model)
    non_existing_detail_url = detail_url_for_model(model, "some-non-existing-id")
    detail_url = detail_url_for_model(model)

    api_test = ApiTest()

    if needs_authentication:
        api_test.put_unauthorized(list_url, {})
        api_test.put_unauthorized(non_existing_detail_url, {})
        api_test.put_unauthorized(detail_url, {})

        if authentication_token:
            api_test.set_bearer_token(authentication_token)
            __test_put_basics(api_test, model)
    else:
        __test_put_basics(api_test, model)


def __test_put_basics(
    api_test: ApiTest,
    model: Model,
):
    list_url = list_url_for_model(model)
    non_existing_detail_url = detail_url_for_model(model, "some-non-existing-id")

    api_test.put_method_not_allowed(list_url, {})
    api_test.put_not_found(non_existing_detail_url, {})


def check_put_not_allowed(
    model: Model,
    authentication_token: Optional[str] = None,
):
    """
    Test that put is not allowed
    """

    list_url = list_url_for_model(model)
    detail_url = detail_url_for_model(model)

    api_test = ApiTest(token=authentication_token)
    api_test.patch_method_not_allowed(list_url, {})
    api_test.patch_method_not_allowed(detail_url, {})


def check_put_parameters_successful(
    model: Model,
    successful_parameters: List[dict],
    authentication_token: Optional[str] = None,
    return_serializer: Optional[Type[Serializer]] = None,
    body_format: RequestBodyFormat = RequestBodyFormat.Json,
):
    """
    Test that a list of parameter updates successfully.

    1. Successful put
    2. Checks the request parameters against the response.
    (3.) Optionally tests the response against a serializer
    """

    url = detail_url_for_model(model)
    api_test = ApiTest(token=authentication_token)

    for successful_put_parameter in successful_parameters:
        response = api_test.put_successful(
            url,
            successful_put_parameter,
            body_format,
        )
        check_object_against_parameter(response, successful_put_parameter)

        if return_serializer:
            model.refresh_from_db()
            assert dictionary_is_serialized_instance(
                instance=model,
                serializer=return_serializer,
                response=response,
            )


def check_put_parameters_failing(
    model: Model,
    failing_parameters: List[dict],
    authentication_token: Optional[str] = None,
    body_format: RequestBodyFormat = RequestBodyFormat.Json,
):
    """
    Test that a list of parameter fails
    """

    url = detail_url_for_model(model)
    api_test = ApiTest(token=authentication_token)

    for failing_put_parameter in failing_parameters:
        api_test.put_bad_request(
            url,
            failing_put_parameter,
            body_format,
        )


def check_put_read_only_field(
    model: Model,
    successful_put_parameter: dict,
    key: str,
    value: Any,
    authentication_token: Optional[str] = None,
    body_format: RequestBodyFormat = RequestBodyFormat.Json,
):
    """
    Check that a put request that includes certain parameter does not have any effect
    """

    successful_put_parameter[key] = value
    api_test = ApiTest(token=authentication_token)

    url = detail_url_for_model(model)
    response = api_test.patch_successful(url, successful_put_parameter, body_format)

    assert response[key] != value


__all__ = [
    "check_put_basics",
    "check_put_not_allowed",
    "check_put_parameters_failing",
    "check_put_parameters_successful",
    "check_put_read_only_field",
]
