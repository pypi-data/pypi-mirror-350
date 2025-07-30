import base64
import random
import string

from django.core.files.base import ContentFile
from rest_framework import serializers


class FileFieldBase64(serializers.FileField):
    """
    Small extension to the file fields that is able to work with Base64 encoded strings
    """

    def to_internal_value(self, data):
        if isinstance(data, str):
            random_name = "".join(
                random.choice(string.ascii_lowercase) for i in range(10)
            )

            data = ContentFile(
                base64.b64decode(data + "==="),
                name=random_name,
            )

        else:
            data = super().to_internal_value(data)

        return data
