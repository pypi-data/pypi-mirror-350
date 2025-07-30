from django.db import models


class BaseModel(models.Model):
    """
    A abstraction over the Django base model.

    The models comes with enabled validation check on save.

    The models also has fields for keeping the created timestamp and an updated
    timestamp.
    """

    created = models.DateTimeField(
        auto_now_add=True,
        null=False,
        blank=True,
        help_text="The time when the model instance was created",
    )

    updated = models.DateTimeField(
        auto_now=True,
        null=False,
        blank=True,
        help_text="The last time the model instance was updated.",
    )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    class Meta:
        abstract = True
