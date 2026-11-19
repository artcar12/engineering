"""Order totals. Amounts are integer cents; discounts are stored as positive integer cents."""

from __future__ import annotations

from typing import Any


def subtotal_cents(order: dict[str, Any]) -> int:
    return sum(line["unit_cents"] * line["quantity"] for line in order["lines"])


def total_cents(order: dict[str, Any]) -> int:
    """The amount the customer pays: the subtotal less any discount, never below zero."""
    subtotal = subtotal_cents(order)
    discount = order.get("discount_cents", 0)
    return max(0, subtotal + discount)
