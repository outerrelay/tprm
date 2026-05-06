from django.db import models

from core.models import AuditedModel, PrefixedIDModel


class Company(PrefixedIDModel, AuditedModel):
    """Canonical legal-entity record.

    A Company exists independently of whether we manage it as a Vendor.
    Non-vendor parent companies, shareholders, and supply-chain participants
    are represented as Companies without a linked Vendor row.
    """

    id_prefix = "CMP"
    id_field = "company_id"

    company_id = models.CharField(max_length=20, unique=True, blank=True, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    country_of_incorporation = models.CharField(max_length=100, blank=True)
    registration_number = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'companies'

    def __str__(self):
        return self.name
