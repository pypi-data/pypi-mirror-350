from typing import Any, List, Tuple, Union

from django.contrib.admin.options import BaseModelAdmin
from django.http.request import HttpRequest


class HiddenFieldsMixin(BaseModelAdmin):
    hidden_fields: Union[List[str], Tuple[str]] = []

    def get_fields(self, request: HttpRequest, obj: Union[Any, None] = ...):
        """
        Exclude all fields that may hold sensitive data
        """

        fields = super().get_fields(request, obj)
        fields_list = list(fields)

        if obj and self.hidden_fields:
            for field in self.hidden_fields:
                fields_list.remove(field)

        return tuple(fields_list)
