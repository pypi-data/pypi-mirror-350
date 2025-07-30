from typing import TYPE_CHECKING

from django.core.files.storage import default_storage

if TYPE_CHECKING:
    from django.core.files.storage import Storage


def file_exists_in_storage(file_path) -> bool:
    storage: "Storage" = default_storage

    return storage.exists(file_path)
