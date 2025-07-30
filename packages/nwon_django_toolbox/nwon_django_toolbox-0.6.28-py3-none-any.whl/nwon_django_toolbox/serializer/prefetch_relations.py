import collections

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


def prefetch_relations(queryset):
    """
    Based on:
    https://andrew.hawker.io/writings/2020/11/18/django-activity-stream-prefetch-generic-foreign-key/

    Prefetch content type relations for GenericForeignKeys to reduce N+1 queries.
    """
    # Get all GenericForeignKey fields on all models of the queryset.
    gfks = _queryset_generic_foreign_keys(queryset)

    # Get mapping of GFK content_type -> list of GFK object_pks for all GFK's on the queryset.
    gfks_data = _content_type_to_content_mapping_for_gfks(queryset, gfks)

    for content_type, object_pks in gfks_data.items():
        # Get all model instances referenced through a GFK.
        gfk_models = prefetch_relations(
            content_type.model_class()
            .objects.filter(pk__in=object_pks)
            .select_related()
        )

        for gfk_model in gfk_models:
            for gfk in _queryset_gfk_content_generator(queryset, gfks):
                qs_model, gfk_field_name, gfk_content_type, gfk_object_pk = gfk

                if gfk_content_type != content_type:
                    continue

                if gfk_object_pk != str(
                    gfk_model.pk
                ):  # str compare otherwise UUID PK's puke. :(
                    continue

                setattr(qs_model, gfk_field_name, gfk_model)

    return queryset


def _queryset_generic_foreign_keys(queryset):
    """
    Build mapping of name -> field for GenericForeignKey fields on the queryset.
    """

    gfks = {}
    for name, field in queryset.model.__dict__.items():
        if not isinstance(field, GenericForeignKey):
            continue

        gfks[name] = field

    return gfks


def _queryset_gfk_content_generator(queryset, gfks):
    """
    Generator function that yields information about all GenericForeignKey fields for all models of a queryset.
    """
    for model in queryset:
        for field_name, field in gfks.items():
            content_type_id = getattr(
                model, field.model._meta.get_field(field.ct_field).get_attname()
            )

            if not content_type_id:
                continue

            content_type = ContentType.objects.get_for_id(content_type_id)

            object_pk = str(getattr(model, field.fk_field))

            yield (model, field_name, content_type, object_pk)


def _content_type_to_content_mapping_for_gfks(queryset, gfks):
    """
    Build mapping of content_type -> [content_pk] for the given queryset and its generic foreign keys.
    """
    data = collections.defaultdict(list)

    for (
        model,
        field_name,
        content_type,
        object_pk,
    ) in _queryset_gfk_content_generator(queryset, gfks):
        data[content_type].append(object_pk)

    return data
