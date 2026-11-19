from app.db import Database


def seeded_db() -> Database:
    d = Database()
    d.insert("tenants", {"id": 1, "name": "Acme"})
    d.insert("tenants", {"id": 2, "name": "Globex"})
    d.insert("customers", {"id": 10, "tenant_id": 1, "name": "Ada"})
    d.insert("customers", {"id": 11, "tenant_id": 1, "name": "Grace"})
    d.insert("customers", {"id": 20, "tenant_id": 2, "name": "Linus"})
    d.insert(
        "orders",
        {"id": 100, "tenant_id": 1, "customer_id": 10, "lines": [{"unit_cents": 500, "quantity": 2}]},
    )
    d.insert(
        "orders",
        {
            "id": 101,
            "tenant_id": 1,
            "customer_id": 11,
            "lines": [{"unit_cents": 250, "quantity": 4}],
            "discount_cents": 100,
        },
    )
    d.insert(
        "orders",
        {"id": 200, "tenant_id": 2, "customer_id": 20, "lines": [{"unit_cents": 9999, "quantity": 1}]},
    )
    return d
