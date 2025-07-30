from typing import Dict, Optional
from urllib.parse import urlencode

from django.db.models import Model
from django.urls import reverse
from django.utils.html import format_html

from nwon_django_toolbox.settings import NWON_DJANGO_SETTINGS
from nwon_django_toolbox.url_helper.url_helper import base_name_from_model


def formatted_django_admin_link(
    model: Model,
    application: str = "nwon",
    link_text: Optional[str] = None,
    parameter: Optional[Dict[str, str]] = None,
) -> str:
    if application is None:
        raise Exception(
            "In order to use django_admin_link_for_model you need to set application_name in the NWON_DJANGO settings"
        )

    url = django_admin_link_for_model(model, application, parameter)

    return format_html(
        "<a href='{url}'>{text}</a>",
        url=url,
        text=link_text if link_text else model.__str__(),
    )


def django_admin_link_for_model(
    model: Model,
    application: Optional[str] = NWON_DJANGO_SETTINGS.application_name,
    parameter: Optional[Dict[str, str]] = None,
) -> str:
    if application is None:
        raise Exception(
            "In order to use django_admin_link_for_model you need to set application_name in the NWON_DJANGO settings"
        )

    url = reverse(
        f"admin:{application}_{base_name_from_model(model)}_change",
        args=(model.pk,),
    )
    if parameter:
        url = f"{url}?{urlencode(parameter)}"

    return url


__all__ = [
    "formatted_django_admin_link",
    "django_admin_link_for_model",
]
