import copy
from typing import Any, List, Optional, Type, Union

from jsonschema_to_openapi.convert import convert as convert_to_openapi
from nwon_baseline.pydantic import pydantic_model_to_dict, schema_from_pydantic_model
from nwon_baseline.typings import AnyDict
from pydantic import ValidationError as PydanticValidationError
from pydantic.main import BaseModel
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import JSONField

__all__ = ["PydanticJsonFieldSerializer"]


class PydanticJsonFieldSerializer(JSONField):
    """
    Serializer for serializing our custom PydanticJsonField.

    Provides annotations for drf-spectacular
    """

    class Meta:
        swagger_schema_fields: AnyDict

    def __init__(
        self, *args, pydantic_models: Optional[List[Type[BaseModel]]] = None, **kwargs
    ):
        super().__init__(*args, **kwargs)

        # Convert list to tuple for caching
        models_tuple = tuple(pydantic_models) if pydantic_models else None
        self.schema = self.__schema_information(models_tuple)

        # Set schema for drf-spectacular
        self.coreapi_schema = convert_to_openapi(copy.deepcopy(self.schema))

        # Set schema for drf-yasg
        PydanticJsonFieldSerializer.Meta.swagger_schema_fields = self.schema

        self.pydantic_models = pydantic_models if pydantic_models else []

    def to_representation(self, value: Any):
        value = super().to_representation(value)

        if value is None:
            return None

        for model in self.pydantic_models:
            try:
                if isinstance(value, dict):
                    return pydantic_model_to_dict(model.model_validate(value))
                elif isinstance(value, BaseModel):
                    return pydantic_model_to_dict(model.model_validate(value))
                else:
                    return pydantic_model_to_dict(model.model_validate_strings(value))
            except PydanticValidationError:
                pass

        # Return raw value or raise error if no model validated
        raise ValidationError("No matching Pydantic model for representation.")

    def to_internal_value(self, data: Any):
        data = super().to_internal_value(data)

        for model in self.pydantic_models:
            try:
                parsed_json = model.model_validate(data)
                return parsed_json.model_dump()
            except PydanticValidationError as error:
                error_details = [
                    {
                        "location": e["loc"],
                        "message": e["msg"],
                        "type": e.get("type", "unknown"),
                    }
                    for e in error.errors()
                ]

                raise ValidationError({"errors": error_details}) from error

        return None

    def __schema_information(
        self, pydantic_models: Optional[tuple[Type[BaseModel], ...]]
    ) -> AnyDict:
        """
        Returns a JSON schema that is used for representing the potential values of this field
        """

        if pydantic_models is None or len(pydantic_models) == 0:
            return {"type": "object"}

        elif len(pydantic_models) > 1:
            return {
                "anyOf": [
                    schema_from_pydantic_model(model) for model in pydantic_models
                ]
            }

        return (
            schema_from_pydantic_model(pydantic_models[0])
            if len(pydantic_models) > 0 and pydantic_models[0]
            else {"type": "object"}
        )


try:
    from drf_spectacular.extensions import OpenApiSerializerFieldExtension

    class PydanticJsonFieldSerializerExtension(OpenApiSerializerFieldExtension):  # type: ignore
        target_class = PydanticJsonFieldSerializer

        def map_serializer_field(self, auto_schema, direction):
            schema = self.target.schema or {"type": "object"}
            return schema

except Exception:
    pass
