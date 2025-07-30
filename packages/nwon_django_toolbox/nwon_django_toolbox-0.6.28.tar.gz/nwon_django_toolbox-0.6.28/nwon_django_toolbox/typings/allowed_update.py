from typing import Any, List, Optional

from pydantic import BaseModel


class AllowedUpdate(BaseModel):
    field_name: str
    """ A field name that can be updated """

    allowed_values: Optional[List[Any]] = None
    """ If set the allowed values for the field are limited to the given values """
