"""Sidebar navigation configuration.

Each section is rendered as a header followed by its links. `path_match` is
the substring matched against `request.path` to mark the link as active.
"""

NAV_SECTIONS = [
    {
        'label': 'Risk Management',
        'items': [
            {
                'label': 'Vendors',
                'url_name': 'vendors:vendor_list',
                'icon': 'bi-building',
                'path_match': '/vendors/',
            },
            {
                'label': 'People',
                'url_name': 'people:person_list',
                'icon': 'bi-people',
                'path_match': '/people/',
            },
        ],
    },
]
