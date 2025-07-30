from typing import Type, Union

from django.db.models import Model
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch


def detail_url_for_model(model: Model, primary_key: Union[str, int, None] = None):
    used_primary_key: Union[str, int] = primary_key if primary_key else model.pk
    return detail_url_for_model_class(model.__class__, used_primary_key)


def detail_url_for_model_class(model: Type[Model], primary_key: Union[str, int]):
    view_name = _base_name_from_model_class(model) + "-detail"

    try:
        url = reverse(
            viewname=view_name,
            kwargs={"pk": primary_key},
        )
    except NoReverseMatch as exception:
        """
        Pretty project specific workaround to make this work with a custom user model
        named CustomUser
        """
        if view_name == "customuser-detail":
            return f"/users/{primary_key}/"

        # Fix for polymorphic child models that don't have their own view
        # We try to find the base model and use its detail view
        if hasattr(model, "__bases__"):
            class_to_use = model.__bases__[0]
            if class_to_use != model:
                return detail_url_for_model_class(class_to_use, primary_key)

        raise exception

    return url


def list_url_for_model_class(model_class: Type[Model]):
    try:
        return reverse(_base_name_from_model_class(model_class) + "-list")
    except NoReverseMatch as exception:
        # Fix for polymorphic child models that don't have their own view
        # We try to find the base model and use its list view
        if hasattr(model_class, "__bases__"):
            class_to_use = model_class.__bases__[0]
            if class_to_use != model_class:
                return list_url_for_model_class(class_to_use)

        raise exception


def list_url_for_model(model: Model):
    return list_url_for_model_class(model.__class__)


def _base_name_from_model_class(model_class: Type[Model]) -> str:
    return model_class.__name__.lower()


def base_name_from_model(model: Model) -> str:
    return _base_name_from_model_class(model.__class__)


__all__ = [
    "detail_url_for_model",
    "detail_url_for_model_class",
    "list_url_for_model_class",
    "list_url_for_model",
    "base_name_from_model",
]
