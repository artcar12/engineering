"""A deliberately tiny in-memory table store.

Every table carries a ``tenant_id`` column. The service runs one shared schema for all tenants,
so callers must always pass ``tenant_id`` when they read — see ``repository.py`` for the helpers
that enforce it.
"""

from __future__ import annotations

from typing import Any


class Database:
    def __init__(self) -> None:
        self.tables: dict[str, list[dict[str, Any]]] = {
            "tenants": [],
            "customers": [],
            "orders": [],
        }
        self.query_count = 0

    def insert(self, table: str, row: dict[str, Any]) -> None:
        self.tables[table].append(dict(row))

    def fetch_all(self, table: str, **where: Any) -> list[dict[str, Any]]:
        """Return every row in ``table`` matching all ``where`` equalities."""
        self.query_count += 1
        return [
            dict(row)
            for row in self.tables[table]
            if all(row.get(k) == v for k, v in where.items())
        ]

    def fetch_one(self, table: str, **where: Any) -> dict[str, Any] | None:
        rows = self.fetch_all(table, **where)
        return rows[0] if rows else None
