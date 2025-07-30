from django.contrib import admin


def custom_titled_filter(title: str, list_filter=admin.FieldListFilter):
    """
    Small wrapper for getting a filter with a custom name
    """

    class Wrapper(list_filter):
        def __new__(cls, *args, **kwargs):
            instance = list_filter.create(*args, **kwargs)
            instance.title = title
            return instance

    return Wrapper
