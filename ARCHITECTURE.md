# TPRM Platform — Architectural Decisions

This file records load-bearing architectural decisions for the TPRM platform: what the rule is, what we considered, and **why** we chose it. Update it when a decision changes; do not delete superseded sections — strike them through and explain.

> If you are an AI assistant: read this file before changing models, adding apps, or designing relationships. The decisions below have already been made; do not re-litigate them without the user's explicit go-ahead.

---

## 1. Apps and where things live

### `core` — abstract bases and shared utilities (no tables)
Contains nothing concrete. Houses:
- [core/models.py](core/models.py): `TimestampedModel`, `AuditedModel`, `PrefixedIDModel` (all abstract)
- [core/mixins.py](core/mixins.py): `AuditMixin` (view mixin — sets `created_by`/`updated_by` from `request.user` on form save)
- [core/forms.py](core/forms.py): `BootstrapFormMixin` — auto-applies `form-control` / `form-select` / `form-check-input` based on widget type
- [core/templatetags/core_extras.py](core/templatetags/core_extras.py): `tier_badge`, `status_badge` filters
- [core/nav.py](core/nav.py) + [core/context_processors.py](core/context_processors.py): centralized sidebar nav config

### `companies` — canonical legal-entity records
A `Company` is a legal entity we know about. Independent of whether we manage it as a vendor.

### `vendors` — vendor-specific role on top of a Company
A Vendor is one-to-one with a Company. Vendor adds tier/status/contact and assessment relationships.

### `people` — Person and Vendor↔Person relationships
`Person` is domain-agnostic. `VendorPersonRelationship` ties a Person to a Vendor with a relationship type (shareholder, key executive, beneficial owner, contact person).

---

## 2. Company / Vendor split

**Rule:** A `Company` is the canonical record. A `Vendor` is a separate model with a `OneToOneField(Company)` plus vendor-specific fields (`tier`, `status`, `contact_name`, `contact_email`, `vendor_id`).

**Why:** Future features need to track Companies that aren't vendors — parent companies, non-vendor shareholders, supply-chain participants. Keeping Company canonical means ownership relationships always point at Company; "promote a Company to a Vendor" is a one-row insert.

**Considered and rejected:**
- *Single `Organization` model with a type field* — vendor-only fields would become nullable noise on every record; weak type safety.
- *Multi-table inheritance (`Vendor(Company)`)* — implicit join on every Vendor query; awkward to demote a Vendor back to a non-vendor Company.
- *Keep them duplicated* — shareholder relationships need both anyway.

**Practical consequences:**
- Code that needs the vendor's display name reads `vendor.company.name`. There are convenience properties on `Vendor` (`vendor.name`, `vendor.description`, `vendor.website`) that delegate to the underlying Company so existing templates keep working, but new code should prefer the explicit `vendor.company.X` form.
- The `VendorForm` ([vendors/forms.py](vendors/forms.py)) collects both Company fields (name/description/website) and Vendor fields (tier/status/contacts). On save, it creates or updates the linked Company in lockstep.
- The split was performed in migration [vendors/migrations/0007_split_company.py](vendors/migrations/0007_split_company.py) with a data migration that backfilled Company rows from existing Vendor data.

---

## 3. Ownership / relationship graph (deferred — design locked)

**Rule (when implemented):** A single `OwnershipRelationship` model in a future `relationships` app, with two `GenericForeignKey` fields (`from_party`, `to_party`) that can point at `Person`, `Company`, or `Vendor`. Fields: `relationship_type` (shareholder, beneficial_owner, parent_company, key_executive, contact_person, supply_chain_link, ...), `ownership_percentage`, `is_active`, `start_date`, `end_date`, `notes`.

**Why:** The same fact-shape applies whether the parties are people, companies, or vendors. Multiple specific tables (Person→Vendor, Company→Vendor, Vendor→Vendor, Person→Company, ...) would explode combinatorially and force UNION queries for any "who owns X?" question.

**Tradeoff accepted:** GenericForeignKey gives up DB-level FK constraints and makes admin slightly clunkier. We accept it for graph uniformity.

**When this is built:**
- Migrate existing `VendorPersonRelationship` rows into `OwnershipRelationship`.
- Drop `VendorPersonRelationship`.
- The graph then handles vendor-to-vendor supply chain links (just a new `relationship_type`, no schema change).

---

## 4. Assessment stays vendor-bound; integrity checks get their own model

**Rule:** `Assessment` keeps its concrete `ForeignKey(Vendor)` and the existing rollup math (`overall_inherent_rating`, `overall_residual_rating`). When automated integrity checks land, they get their own `IntegrityCheck` model with a `GenericForeignKey` subject (Vendor / Person / Company).

**Why:** The rollup math in [vendors/services/ratings.py](vendors/services/ratings.py) is tightly coupled to Vendor and to a fixed list of categories. Generalizing `Assessment` away from Vendor would lose the clean `vendor.assessments` reverse manager and complicate every rollup query.

**When this is built:**
- `IntegrityCheck` lives in a new app (or `core`); `provider` (e.g. `'openai_deep_research'`), `raw_response` (`JSONField`), `summary`, `risk_signal`.
- If the subject is a Vendor, a save handler mirrors the result into an `Assessment` row of category `integrity` so the existing rating math keeps working unchanged.

---

## 5. Domain logic lives in `services/`, not on models

**Rule:** Non-trivial computation (rollup math, scoring, integrations) lives in an app's `services/` package. Model methods/properties are thin wrappers that delegate.

**Why:** Once questionnaires and integrity checks feed into ratings, the rollup logic will grow. Keeping it on the model bloats `models.py` and tangles ORM concerns with business logic.

**Currently applied:**
- [vendors/services/ratings.py](vendors/services/ratings.py) holds `RATING_VALUES`, `CATEGORY_WEIGHTS`, `bucket()`, `overall_inherent_rating()`, `overall_residual_rating()`. Vendor's `overall_*_rating` properties just call into it.

---

## 6. Async / external API infra: deferred

**Rule:** Do not add Celery yet. When external API integrations land (e.g. OpenAI Deep Research for integrity checks), define a single function `core.integrations.<thing>.run_*` that runs synchronously and is invoked from a Django management command. When response times become painful, swap to `django-q2` or `huey` (lightweight, can use the existing DB as the queue, single worker process).

**Why:** Celery needs Redis/RabbitMQ + a worker process + deployment changes — heavy for a SQLite-local app. The interface stays the same when we swap the runner; only the runner changes.

---

## 7. Public/token-based access (deferred — pattern reserved)

**Rule (when implemented):** A `core.views.PublicTokenAccessMixin` will parallel `LoginRequiredMixin`. It validates a signed token from the URL and grants access to a single object. Used for Due Diligence Questionnaire response views where vendors fill in forms without logging in.

**Why:** Every other view requires `LoginRequiredMixin`. Token-gated views should be a clearly-named alternative mixin so the access model is obvious at the view definition site.

---

## 8. Conventions referenced from CLAUDE.md

The following are operational conventions, not architectural decisions — they live in [CLAUDE.md](CLAUDE.md):

- All views are class-based and use `LoginRequiredMixin` (or, in the future, `PublicTokenAccessMixin`).
- All forms inherit `BootstrapFormMixin` from [core/forms.py](core/forms.py).
- All non-abstract models inherit `AuditedModel` (and `PrefixedIDModel` if they have a public-facing ID).
- Custom domain logic goes in `<app>/services/` modules.
- Sidebar nav is configured in [core/nav.py](core/nav.py).
