# TPRM Platform

A third-party risk management platform for tracking vendors, risk assessments, and findings.

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
vendors/                 Core app — Vendor, Assessment, Risk models
  forms.py               Bootstrap-wired ModelForms
  templatetags/          Custom badge filters (tier_badge, status_badge)
  templates/vendors/     App-level page templates
templates/               Global templates (base layout, login page)
manage.py
requirements.txt
```

## Domain Model

- **Vendor** — a third-party entity; has a tier (Critical / High / Medium / Low) and a status
- **Assessment** — a point-in-time risk review for a vendor; has a risk rating and lifecycle status
- **Risk** — an individual finding within an assessment; has severity and remediation status
