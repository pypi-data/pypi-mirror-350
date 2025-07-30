from typing import Union

from django.conf import settings
from django.db.models.fields.files import FieldFile, ImageFieldFile
from django.http import HttpResponseRedirect


def redirect_to_s3_url(field: Union[ImageFieldFile, FieldFile]) -> HttpResponseRedirect:
    url = field.url.replace(settings.AWS_S3_ENDPOINT_URL, settings.AWS_S3_CUSTOM_DOMAIN)
    return HttpResponseRedirect(url)
