from enum import Enum
from typing import Any, List, Tuple


class DjangoReadyEnum(Enum):
    @classmethod
    def choices(cls) -> List[Tuple[Any, str]]:
        return [(key.value, key.name) for key in cls]


__all__ = ["DjangoReadyEnum"]
