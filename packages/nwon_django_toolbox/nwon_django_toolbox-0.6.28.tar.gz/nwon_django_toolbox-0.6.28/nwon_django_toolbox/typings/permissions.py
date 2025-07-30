from enum import Enum
from typing import TYPE_CHECKING, Dict, List, Type, TypeVar

if TYPE_CHECKING:
    from django.contrib.auth.models import Permission
    from django.db.models import Model


class PermissionPrefix(Enum):
    View = "view"
    Change = "change"
    Add = "add"
    Delete = "delete"


T = TypeVar("T", bound=Enum)

PermissionConfigurationForGroup = Dict[PermissionPrefix, List[Type["Model"]]]
PermissionConfiguration = Dict[T, PermissionConfigurationForGroup]
GroupPermissionMapping = Dict[T, List["Permission"]]
