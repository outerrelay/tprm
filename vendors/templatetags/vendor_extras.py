from django import template
from django.utils.safestring import mark_safe

register = template.Library()

_TIER_CSS = {
    'critical': 'bg-danger',
    'high': 'bg-warning text-dark',
    'medium': 'bg-info text-dark',
    'low': 'bg-success',
    'none': 'bg-secondary',
}

_STATUS_CSS = {
    'active': 'bg-success',
    'under_review': 'bg-warning text-dark',
    'offboarded': 'bg-secondary',
    'planned': 'bg-secondary',
    'in_progress': 'bg-primary',
    'completed': 'bg-success',
    'cancelled': 'bg-danger',
    'open': 'bg-danger',
    'accepted': 'bg-warning text-dark',
    'mitigated': 'bg-success',
    'closed': 'bg-secondary',
    'none': 'bg-secondary',
}


@register.filter
def tier_badge(value):
    css = _TIER_CSS.get(value, 'bg-secondary')
    label = value.replace('_', ' ').capitalize() if value else '—'
    return mark_safe(f'<span class="badge {css}">{label}</span>')


@register.filter
def status_badge(value):
    css = _STATUS_CSS.get(value, 'bg-secondary')
    label = value.replace('_', ' ').capitalize() if value else '—'
    return mark_safe(f'<span class="badge {css}">{label}</span>')
