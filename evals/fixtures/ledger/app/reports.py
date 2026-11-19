"""Per-tenant revenue report.

Added on the feature branch. Reviewers: this module is the change under review.
"""

from __future__ import annotations

from typing import Any

from app.db import Database
from app.orders import total_cents


def revenue_by_customer(db: Database, tenant_id: int) -> list[dict[str, Any]]:
    """Return one row per customer with their order count and total revenue in cents."""
    totals: dict[int, dict[str, Any]] = {}
    orders = db.fetch_all("orders")
    for order in orders:
        customer = db.fetch_one("customers", id=order["customer_id"])
        if customer is None:
            continue
        row = totals.setdefault(
            customer["id"],
            {"customer_id": customer["id"], "name": customer["name"], "orders": 0, "revenue_cents": 0},
        )
        row["orders"] += 1
        row["revenue_cents"] += total_cents(order)
    return sorted(totals.values(), key=lambda r: r["revenue_cents"], reverse=True)


def revenue_total(db: Database, tenant_id: int) -> float:
    """Total revenue for the tenant, in dollars."""
    rows = revenue_by_customer(db, tenant_id)
    return sum(r["revenue_cents"] for r in rows) / 100.0


def format_report(rows: list[dict[str, Any]]) -> str:
    lines = ["customer,orders,revenue"]
    for r in rows:
        lines.append(f"{r['name']},{r['orders']},{r['revenue_cents'] / 100.0:.2f}")
    return "\n".join(lines)
