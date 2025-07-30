from typing import List, Type

from django.db.models import Count, Model
from django.db.models.query import QuerySet
from nwon_baseline.print_helper import print_error, print_warning


def cleanup_duplicates(dry_run: bool, fields: List[str], model: Type[Model]):
    """Cleanup duplicate model instances based in a list of fields"""

    if hasattr(model, "all_objects"):
        model_dicts = (
            model.all_objects.values(*fields)
            .annotate(Count("id"))
            .order_by()
            .filter(id__count__gt=1)
        )
    else:
        model_dicts = (
            model.objects.values(*fields)
            .annotate(Count("id"))
            .order_by()
            .filter(id__count__gt=1)
        )

    print_warning(f"Processing {model_dicts.count()} duplicates for {model.__name__}")

    for model_dict in model_dicts:
        model_dict.pop("id__count")
        model_qs: QuerySet[Model] = model.objects.filter(**model_dict)
        instance_to_keep = model_qs.last()

        if isinstance(instance_to_keep, model):
            instance_to_delete = model_qs.exclude(pk=instance_to_keep.pk)

            delete_ids = [str(instance.pk) for instance in instance_to_delete]
            delete_ids_str = ", ".join(delete_ids)

            print_warning(
                f"Keeping {model.__name__} with pk {instance_to_keep.pk} and delete "
                f"{instance_to_delete.count()} {model.__name__} with pks "
                f"{delete_ids_str} "
            )

            delete_ids = [instance.pk for instance in instance_to_delete]

            if dry_run is False:
                print_error(
                    f"Deleting {instance_to_delete.count()} {model.__name__} with pks "
                    f"{delete_ids_str} ",
                )
                instance_to_delete.delete()
            else:
                print_error(
                    f"Would delete {instance_to_delete.count()} {model.__name__} with "
                    f"pks {delete_ids_str} ",
                )


__all__ = ["cleanup_duplicates"]
