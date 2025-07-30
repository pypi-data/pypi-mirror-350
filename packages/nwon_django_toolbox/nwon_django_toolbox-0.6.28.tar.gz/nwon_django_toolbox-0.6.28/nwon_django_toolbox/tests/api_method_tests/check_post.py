import copy
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
from nwon_django_toolbox.url_helper import (
    detail_url_for_model,
    detail_url_for_model_class,
    list_url_for_model_class,
)


def check_post_basics(
    model_class: Type[Model],
    authentication_token: Optional[str] = None,
    body_format=RequestBodyFormat.Json,
    needs_authentication: bool = True,
):
    """
    Helper function that checks basic functionality of a post endpoint

    1. Method not allowed on detail url if needs_authentication == True
    2. Unauthenticated on detail url if needs_authentication == True
    3. Method not allowed on detail url if needs_authentication == True and token is set
    """

    api_test = ApiTest()
    url = detail_url_for_model_class(model_class, "some-non-existing-id")

    if needs_authentication:
        api_test.post_unauthorized(url, {}, body_format)

        if authentication_token:
            api_test.set_bearer_token(authentication_token)
            api_test.post_method_not_allowed(url, {}, body_format)
    else:
        api_test.post_method_not_allowed(url, {}, body_format)


def check_post_not_allowed(
    model_class: Type[Model],
    authentication_token: Optional[str] = None,
):
    """
    Test that post is not allowed
    """

    list_url = list_url_for_model_class(model_class)

    api_test = ApiTest(token=authentication_token)
    api_test.post_method_not_allowed(list_url, {})


def check_post_parameters_successful(
    model_class: Type[Model],
    successful_parameters: List[dict],
    authentication_token: Optional[str] = None,
    return_serializer: Optional[Type[Serializer]] = None,
    body_format=RequestBodyFormat.Json,
):
    """
    Test that a list of parameter create successfully.

    1. Successful create
    2. Checks the request parameters against the response.
    3. Checks the request parameters against the object returned from get endpoint.
    (4.) Optionally tests the response against a serializer
    """

    list_url = list_url_for_model_class(model_class)
    api_test = ApiTest(token=authentication_token)

    for successful_parameter in successful_parameters:
        response = api_test.post_create_successful(
            list_url, successful_parameter, body_format=body_format
        )
        check_object_against_parameter(response, successful_parameter)

        created_object = model_class.objects.last()
        assert isinstance(created_object, model_class)

        if return_serializer:
            assert dictionary_is_serialized_instance(
                instance=created_object,
                serializer=return_serializer,
                response=response,
            )

        url = detail_url_for_model(created_object)
        object_to_check = api_test.get_successful(url)
        check_object_against_parameter(object_to_check, successful_parameter)


def check_post_parameters_required(
    model_class: Type[Model],
    successful_parameter: dict,
    required_keys: List[str],
    authentication_token: Optional[str] = None,
    body_format=RequestBodyFormat.Json,
):
    """
    Test whether a certain parameter is required. First a successful requests verifies
    the parameters. Afterwards the key that should be required is left out and should
    lead to a failing request.
    """

    list_url = list_url_for_model_class(model_class)
    api_test = ApiTest(token=authentication_token)

    # make sure that parameter are working
    api_test.post_create_successful(
        list_url, successful_parameter, body_format=body_format
    )

    for key in required_keys:
        parameter = copy.deepcopy(successful_parameter)
        parameter.pop(key)
        api_test.post_bad_request(list_url, parameter, body_format=body_format)


def check_post_parameters_not_required(
    model_class: Type[Model],
    successful_parameter: dict,
    required_keys: List[str],
    authentication_token: Optional[str] = None,
    body_format=RequestBodyFormat.Json,
):
    """
    Test whether a certain parameter is NOT required. First a successful requests verifies
    the parameters. Afterwards the key that shouldn't be required is left out and should
    still lead to a successful request.
    """

    list_url = list_url_for_model_class(model_class)
    api_test = ApiTest(token=authentication_token)

    # make sure that parameter are working
    api_test.post_create_successful(
        list_url, successful_parameter, body_format=body_format
    )

    for key in required_keys:
        parameter = copy.deepcopy(successful_parameter)
        parameter.pop(key)
        api_test.post_create_successful(list_url, parameter, body_format=body_format)


def check_post_parameters_failing(
    model_class: Type[Model],
    failing_parameters: List[dict],
    authentication_token: Optional[str] = None,
    body_format=RequestBodyFormat.Json,
):
    """
    Test whether certain parameters are failing.
    """

    list_url = list_url_for_model_class(model_class)
    api_test = ApiTest(token=authentication_token)

    for failing_parameter in failing_parameters:
        api_test.post_bad_request(list_url, failing_parameter, body_format=body_format)


def check_post_read_only_field(
    model_class: Type[Model],
    successful_post_parameter: dict,
    key: str,
    value: Any,
    authentication_token: Optional[str] = None,
    body_format=RequestBodyFormat.Json,
):
    """
    Test whether the inclusion of some parameter does not have an effect
    """

    successful_post_parameter[key] = value

    list_url = list_url_for_model_class(model_class)
    api_test = ApiTest(token=authentication_token)

    created_object = api_test.post_create_successful(
        list_url, successful_post_parameter, body_format=body_format
    )

    # check whether read only key was set
    assert created_object[key] != value


__all__ = [
    "check_post_basics",
    "check_post_not_allowed",
    "check_post_parameters_failing",
    "check_post_parameters_successful",
    "check_post_read_only_field",
    "check_post_parameters_not_required",
]
