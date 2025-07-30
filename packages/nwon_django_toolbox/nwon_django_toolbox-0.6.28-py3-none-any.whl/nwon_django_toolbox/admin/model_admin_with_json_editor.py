from django import forms
from django.contrib import admin
from django.db import models
from django_json_widget.widgets import JSONEditorWidget
from polymorphic.admin import PolymorphicChildModelAdmin, PolymorphicParentModelAdmin

from nwon_django_toolbox.fields import PydanticJsonField


class PolymorphicParentModelAdminWithJsonEditor(PolymorphicParentModelAdmin):
    formfield_overrides = {
        models.JSONField: {"widget": JSONEditorWidget},
        PydanticJsonField: {"widget": JSONEditorWidget},
    }


class PolymorphicChildModelAdminWithJsonEditor(PolymorphicChildModelAdmin):
    formfield_overrides = {
        models.JSONField: {"widget": JSONEditorWidget},
        PydanticJsonField: {"widget": JSONEditorWidget},
    }


class ModelAdminWithJsonEditor(admin.ModelAdmin):
    formfield_overrides = {
        models.JSONField: {"widget": JSONEditorWidget},
        PydanticJsonField: {"widget": JSONEditorWidget},
    }


class ModelAdminWithJsonEditorReadOnly(admin.ModelAdmin):
    formfield_overrides = {
        models.JSONField: {
            "widget": JSONEditorWidget(options={"mode": "view", "modes": ["view"]})
        },
        PydanticJsonField: {
            "widget": JSONEditorWidget(options={"mode": "view", "modes": ["view"]})
        },
    }


__all__ = [
    "ModelAdminWithJsonEditorReadOnly",
    "ModelAdminWithJsonEditor",
    "PolymorphicParentModelAdminWithJsonEditor",
    "PolymorphicChildModelAdminWithJsonEditor",
]
