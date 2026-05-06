"""Risk-rollup logic for Vendors.

Computes a vendor's overall inherent and residual rating from the latest
assessment in each category, using a weighted average across categories.

Lives outside `models.py` because it grows over time (questionnaire scoring,
integrity-check signals) and shouldn't bloat the model layer.
"""

RATING_VALUES = {'none': 0, 'low': 1, 'medium': 2, 'high': 3, 'critical': 4}

CATEGORY_WEIGHTS = {
    'credit': 0.2,
    'integrity': 0.2,
    'sanctions': 0.2,
    'cyber': 0.2,
    'geopolitical': 0.2,
}


def bucket(score):
    if score < 0.5:
        return 'none'
    if score < 1.5:
        return 'low'
    if score < 2.5:
        return 'medium'
    if score < 3.5:
        return 'high'
    return 'critical'


def _latest_per_category(vendor, attr):
    latest = {}
    for a in vendor.assessments.order_by('-created_at'):
        latest.setdefault(a.category, getattr(a, attr))
    return latest


def overall_inherent_rating(vendor):
    latest = _latest_per_category(vendor, 'inherent_rating')
    if not latest:
        return 'none'
    score = sum(
        RATING_VALUES.get(latest.get(cat, 'none'), 0) * w
        for cat, w in CATEGORY_WEIGHTS.items()
    )
    return bucket(score)


def overall_residual_rating(vendor):
    latest = _latest_per_category(vendor, 'residual_rating')
    if not latest:
        return 'none'
    score = sum(
        RATING_VALUES.get(latest.get(cat, 'none'), 0) * w
        for cat, w in CATEGORY_WEIGHTS.items()
    )
    return bucket(score)
