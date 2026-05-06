from .nav import NAV_SECTIONS


def navigation(request):
    """Injects sidebar navigation config into every template context."""
    return {'nav_sections': NAV_SECTIONS}
