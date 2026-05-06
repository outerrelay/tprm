from django.db import models

from companies.models import Company
from core.models import AuditedModel, PrefixedIDModel

from .services import ratings


class Vendor(PrefixedIDModel, AuditedModel):
    class Tier(models.TextChoices):
        CRITICAL = 'critical', 'Critical'
        HIGH = 'high', 'High'
        MEDIUM = 'medium', 'Medium'
        LOW = 'low', 'Low'

    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        UNDER_REVIEW = 'under_review', 'Under review'
        OFFBOARDED = 'offboarded', 'Offboarded'

    id_prefix = "VND"
    id_field = "vendor_id"

    vendor_id = models.CharField(max_length=20, unique=True, blank=True, editable=False)
    company = models.OneToOneField(
        Company, on_delete=models.CASCADE, related_name='vendor_profile',
    )
    tier = models.CharField(max_length=20, choices=Tier.choices, default=Tier.MEDIUM)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    contact_name = models.CharField(max_length=255, blank=True)
    contact_email = models.EmailField(blank=True)

    class Meta:
        ordering = ['company__name']

    def __str__(self):
        return self.company.name

    @property
    def name(self):
        return self.company.name

    @property
    def description(self):
        return self.company.description

    @property
    def website(self):
        return self.company.website

    @property
    def overall_inherent_rating(self):
        return ratings.overall_inherent_rating(self)

    @property
    def overall_residual_rating(self):
        return ratings.overall_residual_rating(self)


class Assessment(AuditedModel):
    class Status(models.TextChoices):
        PLANNED = 'planned', 'Planned'
        IN_PROGRESS = 'in_progress', 'In progress'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'

    class Category(models.TextChoices):
        CREDIT = 'credit', 'Credit risk'
        INTEGRITY = 'integrity', 'Integrity risk'
        SANCTIONS = 'sanctions', 'Sanctions risk'
        CYBER = 'cyber', 'Cyber risk'
        GEOPOLITICAL = 'geopolitical', 'Geopolitical risk'

    class Rating(models.TextChoices):
        CRITICAL = 'critical', 'Critical'
        HIGH = 'high', 'High'
        MEDIUM = 'medium', 'Medium'
        LOW = 'low', 'Low'
        NONE = 'none', 'None'

    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='assessments')
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=Category.choices, default=Category.CREDIT)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PLANNED)
    inherent_rating = models.CharField(
        max_length=20, choices=Rating.choices, default=Rating.NONE
    )
    residual_rating = models.CharField(
        max_length=20, choices=Rating.choices, default=Rating.NONE, blank=True
    )
    notes = models.TextField(blank=True)
    started_at = models.DateField(null=True, blank=True)
    completed_at = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.vendor.company.name} — {self.get_category_display()}"
