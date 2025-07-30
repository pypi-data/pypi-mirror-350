from typing import List, Optional, Type

from django.db.models import Model
from nwon_baseline.typings import AnyDict
from pydantic import BaseModel
from rest_framework import serializers


class NestedModel(BaseModel):
    key: str
    """ Key that contains the serialized data """

    serializer: Type[serializers.ModelSerializer]
    """ Serializer that is used to save the data """

    model: Type[Model]
    """ Model that should be created/updated for the given key """

    field_on_related_model: Optional[str] = None
    """ Key in the related model that holds the relation to the nested model """

    field_on_main_model: Optional[str] = None
    """ Key in the main model that holds the relation to the nested model """

    primary_key_field_on_serializer: Optional[str] = None
    """ Key in the serializer that holds the primary key for finding an existing model """


class NestedManyModelSerializer(serializers.ModelSerializer):
    """
    A serializer that allows serialization of nested data that have a
    foreign key to the created model.

    Takes care of creating and updating the related models based on the serialized data.
    Make sure that fields are serialized properly.
    """

    class Meta:
        model: Type[Model]
        nested_models: List[NestedModel] = []

    def create(self, validated_data):
        nested_models = self.Meta.nested_models

        create_parameter = self._parameter_for_nested_models(validated_data)
        created_object = super().create(validated_data)

        created_objects: List[Model] = [created_object]

        for nested_model in nested_models:
            key = nested_model.key

            if create_parameter[key]:
                parameters = (
                    create_parameter[key]
                    if isinstance(create_parameter[key], (list, List))
                    else [create_parameter[key]]
                )

                for parameter in parameters:
                    if nested_model.field_on_related_model:
                        parameter[nested_model.field_on_related_model] = (
                            created_object.pk
                        )

                    """ 
                    Turn serialized model instances into a pk value which is usually
                    what we want when we don't handle the nested creation. 

                    Not sure whether this wil bite us somewhere else... 
                    """
                    for key, value in parameter.items():
                        if isinstance(value, Model):
                            parameter[key] = value.pk

                    serializer = nested_model.serializer(data=dict(parameter))
                    if serializer.is_valid():
                        created_objects.append(serializer.save())
                    else:
                        for created_object in created_objects:
                            created_object.delete()

                        raise serializers.ValidationError({key: serializer.errors})

        return created_object

    def update(self, instance: Model, validated_data):
        nested_models = self.Meta.nested_models

        update_parameters = self._parameter_for_nested_models(validated_data)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        for nested_model in nested_models:
            key = nested_model.key

            if update_parameters[key]:
                parameters = (
                    update_parameters[key]
                    if isinstance(update_parameters[key], (list, List))
                    else [update_parameters[key]]
                )

                for parameter in parameters:
                    model_to_update = None

                    primary_key_to_update = (
                        parameter.get(
                            nested_model.primary_key_field_on_serializer, None
                        )
                        if nested_model.primary_key_field_on_serializer is not None
                        else None
                    )

                    if nested_model.field_on_related_model and primary_key_to_update:
                        model_to_update = nested_model.model.objects.get(
                            pk=primary_key_to_update
                        )

                    elif nested_model.field_on_main_model:
                        try:
                            existing_relation_pk = getattr(
                                instance,
                                f"{nested_model.field_on_main_model}_id",
                                None,
                            )

                            if existing_relation_pk:
                                model_to_update = nested_model.model.objects.get(
                                    pk=existing_relation_pk
                                )
                        except nested_model.model.DoesNotExist:
                            pass

                    """ 
                    Turn serialized model instances into a pk value which is usually
                    what we want when we don't handle the nested creation. 

                    Not sure whether this wil bite us somewhere else... 
                    """
                    for key, value in parameter.items():
                        if isinstance(value, Model):
                            parameter[key] = value.pk

                    if nested_model.field_on_related_model:
                        update_parameter = {
                            **dict(parameter),
                            **{nested_model.field_on_related_model: instance.pk},
                        }
                    else:
                        update_parameter = dict(parameter)

                    # Create new instance if no model exists
                    if not model_to_update:
                        update_serializer = nested_model.serializer(
                            data=update_parameter,
                        )
                    else:
                        update_serializer = nested_model.serializer(
                            instance=model_to_update,
                            data=update_parameter,
                            partial=True,
                        )

                    update_serializer.is_valid(raise_exception=True)
                    related_model = update_serializer.save()

                    if nested_model.field_on_main_model:
                        setattr(
                            instance, nested_model.field_on_main_model, related_model
                        )

        instance.save()

        return instance

    def _parameter_for_nested_models(self, validated_data) -> AnyDict:
        """
        Get parameter for nested models and pop them from validated data
        """

        nested_models = self.Meta.nested_models

        parameter = {}
        for attached_model in nested_models:
            key = attached_model.key
            parameter[key] = validated_data.pop(key) if key in validated_data else None

        return parameter
