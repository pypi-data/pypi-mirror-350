from typing import Optional, Type

from django.db.models.base import Model
from rest_framework.serializers import Serializer

from nwon_django_toolbox.tests.api_client.api_test import ApiTest
from nwon_django_toolbox.tests.helper.dictionary_is_serialized_instance import (
    dictionary_is_serialized_instance,
)
from nwon_django_toolbox.url_helper import detail_url_for_model, list_url_for_model


def check_get_basics(
    model: Model,
    authentication_token: Optional[str] = None,
    return_serializer: Optional[Type[Serializer]] = None,
    needs_authentication: bool = True,
):
    """
    Helper function that checks basic functionality of a get endpoint

    1. Unauthorized on list and detail if needs_authentication == True
    2. Successful request on list and detail with token or without if needs_authentication == True
    (3.) Optional check of responses against serializer
    """

    api_test = ApiTest()

    if needs_authentication:
        list_url = list_url_for_model(model)
        non_existent_detail_url = detail_url_for_model(model, "some-non-existing-id")

        api_test.get_unauthorized(list_url)
        api_test.get_unauthorized(non_existent_detail_url)

        if authentication_token:
            api_test.set_bearer_token(authentication_token)
            __basic_get_test(api_test, model, return_serializer)
    else:
        __basic_get_test(api_test, model, return_serializer)


def __basic_get_test(
    api_test: ApiTest,
    model: Model,
    return_serializer: Optional[Type[Serializer]] = None,
):
    list_url = list_url_for_model(model)
    non_existent_detail_url = detail_url_for_model(model, "some-non-existing-id")
    detail_url = detail_url_for_model(model)

    api_test.get_not_found(non_existent_detail_url)

    response_list = api_test.get_successful(list_url)

    response_detail = api_test.get_successful(detail_url)

    if return_serializer:
        assert dictionary_is_serialized_instance(
            instance=model,
            serializer=return_serializer,
            response=response_list["results"][0],
        )

        assert dictionary_is_serialized_instance(
            instance=model,
            serializer=return_serializer,
            response=response_detail,
        )


__all__ = [
    "check_get_basics",
]
