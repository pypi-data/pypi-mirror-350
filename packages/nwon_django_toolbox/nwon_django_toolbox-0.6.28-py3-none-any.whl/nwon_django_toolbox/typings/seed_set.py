from typing import List, Union

from django.db.models import Model, base
from pydantic import BaseModel, ConfigDict


class SeedSet(BaseModel):
    models: List[Union[Model, base.ModelBase]]
    seed_name: str

    model_config = ConfigDict(arbitrary_types_allowed=True)
