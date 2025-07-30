import json
from typing import Any, Generic, List, Optional, Type, TypeVar, Union

from django.core.exceptions import ValidationError
from django.db.models import JSONField
from nwon_baseline.pydantic import pydantic_model_to_dict
from nwon_baseline.typings import AnyDict
from pydantic import BaseModel
from pydantic import ValidationError as PydanticValidationError

PydanticModel = TypeVar("PydanticModel", bound=BaseModel)


class PydanticJsonField(JSONField, Generic[PydanticModel]):
    """
    An extension of a JSONField that uses a pydantic model for data validation.
    """

    pydantic_model: Optional[Type[PydanticModel]] = None

    def __init__(
        self, *args, pydantic_model: Optional[Type[PydanticModel]] = None, **kwargs
    ):
        self.pydantic_model = pydantic_model
        if self.pydantic_model is not None and not issubclass(
            self.pydantic_model, BaseModel
        ):
            raise TypeError(
                "Parameter pydantic_model must be set and must be valid Pydantic model"
            )

        super().__init__(*args, **kwargs)

    def __get__(self, instance, owner) -> Optional[AnyDict]:  # type: ignore
        """Ensure correct type hinting when accessing the field on a model instance."""
        return super().__get__(instance, owner)  # type: ignore

    def validate(
        self, value: Optional[Union[BaseModel, AnyDict, None]], model_instance
    ):
        if isinstance(value, str):
            value = json.loads(value)

        if value is None:
            super().validate(value, model_instance)
        else:
            if isinstance(value, dict):
                super().validate(value, model_instance)
            else:
                super().validate(pydantic_model_to_dict(value), model_instance)

        self._validate_schema(value)

    def from_db_value(self, value, expression, connection) -> Optional[AnyDict]:
        """
        Directly returns the value. Problem when returning a
        Pydantic model (which is what we want) is that it is not JSON serializable.

        Which is problematic in the context of seed data creation for example.
        """

        if isinstance(value, str):
            value = json.loads(value)

        return value

    def to_python(self, value: Any) -> Optional[AnyDict]:
        """
        Directly returns the value. Problem when returning a
        Pydantic model (which is what we want) is that it is not JSON serializable.
        """

        if isinstance(value, BaseModel):
            return pydantic_model_to_dict(value)

        return value

    def get_prep_value(self, value):
        """
        Before saving the value we make sure it is a dictionary.

        Has the advantage that you can pass in a Pydantic model and it will be
        converted to a dictionary automatically.
        """

        if isinstance(value, BaseModel):
            return pydantic_model_to_dict(value)
        if isinstance(value, dict):
            return value
        if isinstance(value, str):
            return value
        if value is None:
            return None

        raise ValueError(f"Cannot store {type(value)} in {self.name}")

    def _validate_schema(
        self, value: Union[str, AnyDict, BaseModel, None]
    ) -> Optional[PydanticModel]:
        """
        Validates the value against the provided Pydantic model.
        Return the Pydantic model instance or raises ValidationError.
        """

        # Skip validation during fake migrations
        if self.model.__module__ == "__fake__":
            return value  # type: ignore

        if value is None or self.pydantic_model is None:
            return None

        errors: List[str] = []

        try:
            if isinstance(value, str):
                return self.pydantic_model.model_validate_json(value)
            else:
                return self.pydantic_model.model_validate(value)

        except PydanticValidationError as exc:
            errors.append(
                f"JSON does not fit Pydantic model {self.pydantic_model.__name__} {format(exc)}"
            )

        # Raise a validation error if no model matches
        raise ValidationError(
            f"Value does not match any Pydantic model: {errors}", code="invalid"
        )
