# TPRM Platform

A third-party risk management platform for tracking vendors, companies, people, and risk assessments.

## Tech Stack

| Layer | Choice |
|-------|--------|
| Framework | Django 5 |
| Database | SQLite (local) |
| Styling | Bootstrap 5 (CDN) |
| Package management | pip + venv |

## Setup

### Prerequisites

- Python 3.11 or higher

### Installation

1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate       # Windows: .venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Apply database migrations:
   ```bash
   python manage.py migrate
   ```

4. Create an admin account:
   ```bash
   python manage.py createsuperuser
   ```

5. Start the development server:
   ```bash
   python manage.py runserver
   ```

6. Open http://localhost:8000 in your browser and sign in.

## Admin Interface

Django's built-in admin is available at http://localhost:8000/admin — useful for bulk edits and data management.

## Project Structure

```
config/                  Django project (settings, root URLs, WSGI)
core/                    Abstract bases and shared utilities (no DB tables)
  models.py              TimestampedModel, AuditedModel, PrefixedIDModel
  forms.py               BootstrapFormMixin
  nav.py                 Sidebar navigation config
companies/               Canonical Company records (legal entities)
vendors/                 Vendor (one-to-one with Company) + Assessment models
  services/ratings.py    Risk-rollup logic
  templates/vendors/     App-level page templates
people/                  Person entities and VendorPersonRelationship
  templates/people/      App-level page templates
templates/               Global templates (base layout, login page)
manage.py
requirements.txt
```

## Domain Model

- **Company** — a legal entity; canonical record for any third party (`CMP-NNNN`)
- **Vendor** — the vendor role for a Company; holds tier (Critical / High / Medium / Low), status, and contact info (`VND-NNNN`)
- **Assessment** — a point-in-time risk review for a vendor; categories include Credit, Integrity, Sanctions, Cyber, and Geopolitical; carries inherent and residual ratings
- **Person** — an individual associated with one or more vendors (`PER-NNNN`)
- **VendorPersonRelationship** — links a Person to a Vendor with a relationship type (Shareholder, Key executive, Beneficial owner, Contact person) and optional ownership percentage
