from django import template
from django.utils.safestring import mark_safe

register = template.Library()

_RELATIONSHIP_CSS = {
    'shareholder': 'badge-tac-info',
    'key_executive': 'badge-tac-warn',
    'beneficial_owner': 'badge-tac-critical',
    'contact_person': 'badge-tac-ok',
}

_RELATIONSHIP_LABELS = {
    'shareholder': 'Shareholder',
    'key_executive': 'Key executive',
    'beneficial_owner': 'Beneficial owner',
    'contact_person': 'Contact person',
}


@register.filter
def relationship_type_badge(value):
    css = _RELATIONSHIP_CSS.get(value, 'bg-secondary')
    label = _RELATIONSHIP_LABELS.get(
        value,
        value.replace('_', ' ').capitalize() if value else '—',
    )
    return mark_safe(f'<span class="badge {css}">{label}</span>')


@register.filter
def relationship_type_label(value):
    return _RELATIONSHIP_LABELS.get(
        value,
        value.replace('_', ' ').capitalize() if value else '—',
    )
