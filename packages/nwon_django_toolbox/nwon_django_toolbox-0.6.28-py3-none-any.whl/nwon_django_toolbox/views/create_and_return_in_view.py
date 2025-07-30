from typing import Any, Dict, Optional, Type

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from nwon_django_toolbox.views.prefetched_response import prefetched_response


def create_and_return_in_view(
    request: Request,
    create_serializer: Type[Serializer],
    return_serializer: Type[Serializer],
    create_context: Optional[Dict[str, Any]] = None,
) -> Response:
    """
    A helper function that is supposed to be used in a create view.

    It takes an create_serializer that serializes the request.data
    and returns the updated model instance via the return_serializer.
    """

    context = {"request": request}
    if create_context:
        context = {**context, **create_context}

    serializer = create_serializer(data=request.data, context=context)

    if serializer.is_valid():
        created_instance = serializer.save()
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return prefetched_response(
        created_instance, return_serializer, status=status.HTTP_201_CREATED
    )
