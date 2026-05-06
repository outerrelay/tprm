# TPRM Platform — Claude Guide

## Architecture

**Read [ARCHITECTURE.md](ARCHITECTURE.md) before changing models, adding apps, or designing relationships.** It records the canonical decisions on the Company/Vendor split, ownership graph, abstract base models, and where domain logic lives — with the rationale for each. Don't re-litigate those decisions without the user's go-ahead.

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
core/                    Abstract bases and shared utilities (no tables)
  models.py              TimestampedModel, AuditedModel, PrefixedIDModel
  mixins.py              AuditMixin (view mixin)
  forms.py               BootstrapFormMixin (auto-applies form-control etc.)
  nav.py                 NAV_SECTIONS — sidebar configuration
  context_processors.py  Injects nav_sections into every template
  templatetags/
    core_extras.py       tier_badge, status_badge filters
companies/               Canonical Company records (legal entities)
vendors/                 Vendor (OneToOne with Company) + Assessment
  services/ratings.py    Risk-rollup logic (kept off the model)
people/                  Person + VendorPersonRelationship
templates/               Global templates
  base.html              Base layout (navbar, sidebar driven by nav_sections)
  registration/          Django auth templates (login.html)
```

## Key conventions

- **Views**: always class-based, always use `LoginRequiredMixin`. For audit fields, mix in `core.mixins.AuditMixin` on Create/Update views.
- **Forms**: inherit `core.forms.BootstrapFormMixin` (in addition to `forms.ModelForm`). Don't set `class="form-control"` on widgets manually — the mixin handles it.
- **Models**: inherit `core.models.AuditedModel` for created_at/updated_at/created_by/updated_by. If the model needs a public-facing prefixed id (e.g. `VND-XXXX`), also inherit `PrefixedIDModel` and set `id_prefix` and `id_field` class attrs.
- **Domain logic**: lives in `<app>/services/<topic>.py`, not on the model. Models stay thin.
- **Templates**: all extend `base.html`; use `{% load core_extras %}` for badge filters.
- **Sidebar nav**: configured in [core/nav.py](core/nav.py) — append a section/item there, no template edits needed.
- **URL references**: always namespaced — `{% url 'vendors:vendor_list' %}`, `reverse_lazy('vendors:...')`.
- **Models (cont.)**: define `__str__` and `Meta.ordering`; use `TextChoices` for all enum fields.
- **No raw SQL** — use the Django ORM.

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
