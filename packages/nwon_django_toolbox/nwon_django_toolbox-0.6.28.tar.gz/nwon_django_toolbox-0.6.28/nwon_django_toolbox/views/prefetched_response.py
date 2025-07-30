from typing import Type

from django.db.models import Model
from rest_framework import status as rest_status
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from nwon_django_toolbox.serializer.eager_loading_mixin import EagerLoadingMixin


def prefetched_response(
    model: Model, serializer: Type[Serializer], status=rest_status.HTTP_200_OK
):
    """
    A helper function that should be used to return a serialized instance
    in an API view.

    It basically ensures that eager loading (prefetching) is enforced before
    serializing the instance
    """

    query_set = model.__class__.objects.filter(pk=model.pk)

    if issubclass(serializer, EagerLoadingMixin):
        query_set = serializer.setup_eager_loading(query_set)

    return Response(
        serializer(query_set, many=True).data[0],
        status=status,
    )
