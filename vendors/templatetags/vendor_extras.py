from django import template
from django.utils.safestring import mark_safe

register = template.Library()

_TIER_CSS = {
    'critical': 'badge-tac-critical',
    'high': 'badge-tac-high',
    'medium': 'badge-tac-medium',
    'low': 'badge-tac-ok',
    'none': 'badge-tac-off',
}

_STATUS_CSS = {
    'active': 'badge-tac-ok',
    'under_review': 'badge-tac-warn',
    'offboarded': 'badge-tac-off',
    'planned': 'badge-tac-off',
    'in_progress': 'badge-tac-info',
    'completed': 'badge-tac-ok',
    'cancelled': 'badge-tac-critical',
    'open': 'badge-tac-critical',
    'accepted': 'badge-tac-warn',
    'mitigated': 'badge-tac-ok',
    'closed': 'badge-tac-off',
    'none': 'badge-tac-off',
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
