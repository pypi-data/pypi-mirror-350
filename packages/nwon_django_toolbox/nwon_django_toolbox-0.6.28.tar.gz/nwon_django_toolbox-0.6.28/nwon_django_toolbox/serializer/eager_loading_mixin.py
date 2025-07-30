from typing import List, Union

from django.db.models import Prefetch

from nwon_django_toolbox.serializer.prefetch_relations import prefetch_relations


class EagerLoadingMixin:
    SELECT: List[str]
    PREFETCH: List[Union[str, Prefetch]]

    @classmethod
    def setup_eager_loading(cls, queryset):
        queryset = prefetch_relations(queryset)

        if hasattr(cls, "SELECT"):
            queryset = queryset.select_related(*cls.SELECT)

        if hasattr(cls, "PREFETCH"):
            queryset = queryset.prefetch_related(*cls.PREFETCH)

        return queryset
