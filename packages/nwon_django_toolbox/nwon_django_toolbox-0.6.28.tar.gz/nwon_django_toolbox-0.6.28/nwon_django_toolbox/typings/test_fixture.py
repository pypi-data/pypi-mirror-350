from nwon_django_toolbox.typings.pydantic_base_django import PydanticBaseDjango


class Fixture(PydanticBaseDjango):
    path: str
    name_model: str
    preserve_password: bool
