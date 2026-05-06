from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from core.models import AuditedModel, PrefixedIDModel
from vendors.models import Vendor


class Person(PrefixedIDModel, AuditedModel):
    id_prefix = "PER"
    id_field = "person_id"

    person_id = models.CharField(max_length=20, unique=True, blank=True, editable=False)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=40, blank=True)
    country_of_residence = models.CharField(max_length=100, blank=True)
    nationality = models.CharField(
        max_length=255, blank=True,
        help_text="One or more nationalities, comma-separated.",
    )
    date_of_birth = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        mid = f" {self.middle_name}" if self.middle_name else ""
        return f"{self.first_name}{mid} {self.last_name}".strip()

    @property
    def full_name(self):
        return str(self)

    @property
    def nationalities_list(self):
        return [n.strip() for n in self.nationality.split(',') if n.strip()]


class VendorPersonRelationship(AuditedModel):
    class RelationshipType(models.TextChoices):
        SHAREHOLDER = 'shareholder', 'Shareholder'
        KEY_EXECUTIVE = 'key_executive', 'Key executive'
        BENEFICIAL_OWNER = 'beneficial_owner', 'Beneficial owner'
        CONTACT_PERSON = 'contact_person', 'Contact person'

    vendor = models.ForeignKey(
        Vendor, on_delete=models.CASCADE, related_name='person_links',
    )
    person = models.ForeignKey(
        Person, on_delete=models.CASCADE, related_name='vendor_links',
    )
    relationship_type = models.CharField(
        max_length=30, choices=RelationshipType.choices,
    )
    title = models.CharField(max_length=150, blank=True)
    ownership_percentage = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    is_primary_contact = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-is_active', 'vendor__company__name', 'person__last_name']
        constraints = [
            models.UniqueConstraint(
                fields=['vendor', 'person', 'relationship_type'],
                name='uniq_vendor_person_role',
            ),
        ]

    def __str__(self):
        return f"{self.person} — {self.vendor.company.name} ({self.get_relationship_type_display()})"

    def clean(self):
        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValidationError({'end_date': 'End date must be on or after start date.'})
