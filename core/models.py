from django.conf import settings
from django.db import models


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AuditedModel(TimestampedModel):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        on_delete=models.SET_NULL, editable=False, related_name='+',
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        on_delete=models.SET_NULL, editable=False, related_name='+',
    )

    class Meta:
        abstract = True


class PrefixedIDModel(models.Model):
    """Abstract base that auto-fills a human-readable prefix-NNNN id field on save.

    Subclasses must declare:
        id_prefix: the prefix (e.g. "VND")
        id_field:  the name of the CharField to populate (e.g. "vendor_id")
    """

    id_prefix = ""
    id_field = "public_id"

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not getattr(self, self.id_field, None):
            cls = type(self)
            last = cls.objects.order_by('id').last()
            next_num = (last.pk if last else 0) + 1
            setattr(self, self.id_field, f"{self.id_prefix}-{next_num:04d}")
        super().save(*args, **kwargs)
