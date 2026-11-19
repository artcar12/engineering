"""Tenant-scoped query helpers. All reads go through here so the tenant filter cannot be forgotten."""

from __future__ import annotations

from typing import Any

from app.db import Database


def orders_for_tenant(db: Database, tenant_id: int) -> list[dict[str, Any]]:
    return db.fetch_all("orders", tenant_id=tenant_id)


def customers_for_tenant(db: Database, tenant_id: int) -> list[dict[str, Any]]:
    return db.fetch_all("customers", tenant_id=tenant_id)


def customers_by_id(db: Database, tenant_id: int) -> dict[int, dict[str, Any]]:
    """One query, then an index — the pattern to use when joining orders to customers."""
    return {c["id"]: c for c in customers_for_tenant(db, tenant_id)}
