from typing import Optional, OrderedDict, Type

from django.core.files.base import ContentFile
from django.db.models import Model
from rest_framework import serializers


class FileModelSerializer(serializers.ModelSerializer):
    """
    A serializer that allows giving a filename to a file that was uploaded
    as an base64 string.
    """

    class Meta:
        model: Type[Model]
        file_key: Optional[str] = None
        """ Key that holds the file """

        file_name_key: Optional[str] = None
        """ Key that holds the file name """

    def validate(self, attrs: OrderedDict):
        """Assign file name to file validating input data"""

        if not self.Meta.file_key or not self.Meta.file_name_key:
            raise Exception(
                "For a FileModelSerializer you have to define a file_key and a file_name_key"
            )

        validated_data = super().validate(attrs)

        file_name_key = self.Meta.file_name_key
        file_key = self.Meta.file_key

        if hasattr(validated_data, file_key) and hasattr(validated_data, file_name_key):
            file_name = validated_data[file_name_key]
            file = validated_data[file_key]

            if file_name and file:
                if isinstance(file, ContentFile):
                    file.name = file_name
                    validated_data[file_key] = file

            del validated_data[file_name_key]

        return validated_data
