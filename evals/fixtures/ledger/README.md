# Ledger

A small order-ledger service used as an eval fixture. Orders belong to a tenant; every query is scoped by `tenant_id` so one tenant can never recieve another tenant's rows.

## Layout

- `app/db.py` — an in-memory table store with the `tenant_id` convention.
- `app/orders.py` — order totals and discounts.
- `app/repository.py` — the tenant-scoped query helpers every module is expected to use.
- `app/reports.py` — per-tenant revenue report (feature branch).
- `tests/` — pytest suite. Run with `python3 -m unittest -q`.
