from django.db import models

_RATING_VALUES = {'none': 0, 'low': 1, 'medium': 2, 'high': 3, 'critical': 4}
_CATEGORY_WEIGHTS = {
    'credit': 0.2,
    'integrity': 0.2,
    'sanctions': 0.2,
    'cyber': 0.2,
    'geopolitical': 0.2,
}


def _bucket(score):
    if score < 0.5:
        return 'none'
    if score < 1.5:
        return 'low'
    if score < 2.5:
        return 'medium'
    if score < 3.5:
        return 'high'
    return 'critical'


class Vendor(models.Model):
    class Tier(models.TextChoices):
        CRITICAL = 'critical', 'Critical'
        HIGH = 'high', 'High'
        MEDIUM = 'medium', 'Medium'
        LOW = 'low', 'Low'

    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        UNDER_REVIEW = 'under_review', 'Under review'
        OFFBOARDED = 'offboarded', 'Offboarded'

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    tier = models.CharField(max_length=20, choices=Tier.choices, default=Tier.MEDIUM)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    website = models.URLField(blank=True)
    contact_name = models.CharField(max_length=255, blank=True)
    contact_email = models.EmailField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def overall_inherent_rating(self):
        latest = {}
        for a in self.assessments.order_by('-created_at'):
            latest.setdefault(a.category, a.inherent_rating)
        if not latest:
            return 'none'
        score = sum(
            _RATING_VALUES.get(latest.get(cat, 'none'), 0) * w
            for cat, w in _CATEGORY_WEIGHTS.items()
        )
        return _bucket(score)

    @property
    def overall_residual_rating(self):
        latest = {}
        for a in self.assessments.order_by('-created_at'):
            latest.setdefault(a.category, a.residual_rating)
        if not latest:
            return 'none'
        score = sum(
            _RATING_VALUES.get(latest.get(cat, 'none'), 0) * w
            for cat, w in _CATEGORY_WEIGHTS.items()
        )
        return _bucket(score)


class Assessment(models.Model):
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.vendor.name} — {self.get_category_display()}"
