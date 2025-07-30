from typing import List, Optional

from pydantic import AliasGenerator, BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class NWONDjangoTestSettings(BaseModel):
    keys_to_skip_on_api_test: List[str] = Field(
        default=[],
        description="On some API test helper we check the returned objects against the initial parameters. During this check the given keys are skipped",
    )


class NWONDjangoSettings(BaseModel):
    """
    Settings for the NWON-django-toolbox package.

    These can be set in the Django configuration by using the key NWON_DJANGO and
    providing a dictionary that resembles this schema.
    """

    authorization_prefix: str = Field(
        default="Bearer",
        description="Authorization prefix for API calls",
    )

    logger_name: str = Field(
        default="nwon-django",
        description="Logger that is used in the whole package",
    )

    file_encoding: str = Field(
        default="utf-8",
        description="Default File encoding used for all file operations",
    )

    application_name: Optional[str] = Field(
        default=None,
        description="Application name that is used whenever needed",
    )

    api_docs_url: Optional[str] = Field(
        default=None,
        description="Url to the API docs. Used for error handler",
    )

    tests: Optional[NWONDjangoTestSettings] = Field(
        default=None,
        description="Test related configurations",
    )

    model_config = ConfigDict(
        alias_generator=AliasGenerator(validation_alias=to_camel),
        populate_by_name=True,
        extra="forbid",
    )


__all__ = ["NWONDjangoSettings", "NWONDjangoTestSettings"]
