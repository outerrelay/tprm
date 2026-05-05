# TPRM Platform — Claude Guide

## Stack

| Layer | Choice | Reason |
|-------|--------|--------|
| Framework | Django 5 | Built-in ORM, admin, auth, migrations |
| Database | SQLite (local) | Zero-config for development |
| Styling | Bootstrap 5 via CDN | No build step needed |
| Package manager | pip + venv | Standard Python toolchain |

## Project layout

```
config/                  Django project settings, root URLs, WSGI
vendors/                 First-party app: Vendor, Assessment, Risk
  models.py              Domain models
  forms.py               ModelForms with Bootstrap widget attrs
  views.py               Class-based views
  urls.py                URL patterns (namespaced: app_name = 'vendors')
  admin.py               Admin registrations
  templatetags/          Custom template filters
    vendor_extras.py     tier_badge, status_badge filters
  templates/vendors/     App-level templates
templates/               Global templates
  base.html              Base layout (navbar, sidebar, Bootstrap CDN)
  registration/          Django auth templates (login.html)
```

## Key conventions

- **Views**: always class-based, always use `LoginRequiredMixin`
- **Forms**: defined in `forms.py` with Bootstrap `attrs` on each widget — never use `fields = [...]` on the view class directly
- **Templates**: all extend `base.html`; use `{% load vendor_extras %}` for badge filters
- **URL references**: always namespaced — `{% url 'vendors:vendor_list' %}`, `reverse_lazy('vendors:...')`
- **Models**: define `__str__` and `Meta.ordering`; use `TextChoices` for all enum fields
- **No raw SQL** — use the Django ORM

## Running locally

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## After editing models

```bash
python manage.py makemigrations
python manage.py migrate
```

Never commit `db.sqlite3`.

## Adding a new Django app

```bash
python manage.py startapp <name>
```

Then:
1. Add `'<name>.apps.<Name>Config'` to `INSTALLED_APPS` in `config/settings.py`
2. Create `<name>/urls.py` with `app_name = '<name>'`
3. Wire it into `config/urls.py`
4. Create `<name>/templates/<name>/` for app-level templates
