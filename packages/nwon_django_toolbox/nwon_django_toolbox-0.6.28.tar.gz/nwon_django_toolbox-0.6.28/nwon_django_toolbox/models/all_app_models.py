from typing import Optional

from django.apps import apps

from nwon_django_toolbox.settings import NWON_DJANGO_SETTINGS

DEFAULT_APP_NAME = (
    NWON_DJANGO_SETTINGS.application_name
    if NWON_DJANGO_SETTINGS.application_name
    else "nwon"
)


def all_app_models(app_name: str = DEFAULT_APP_NAME):
    return apps.get_app_config(app_name).get_models()
