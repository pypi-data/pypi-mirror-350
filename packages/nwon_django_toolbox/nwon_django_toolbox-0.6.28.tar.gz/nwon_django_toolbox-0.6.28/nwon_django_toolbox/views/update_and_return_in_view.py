from typing import Type

from django.db.models import Model
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from nwon_django_toolbox.views.prefetched_response import prefetched_response


def update_and_return_in_view(
    instance: Model,
    request: Request,
    update_serializer: Type[Serializer],
    return_serializer: Type[Serializer],
    partial: bool = False,
) -> Response:
    """
    A helper function that is supposed to be used in an update view.

    It takes an update_serializer that serializes the request.data
    and returns the updated model instance via the return_serializer.
    """

    serializer = update_serializer(
        data=request.data,
        instance=instance,
        partial=partial,
        context={"request": request},
    )

    if serializer.is_valid():
        updated_instance = serializer.save()
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return prefetched_response(updated_instance, return_serializer)
