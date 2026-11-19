import unittest

from app.reports import format_report, revenue_by_customer
from tests.support import seeded_db


class RevenueReport(unittest.TestCase):
    def test_report_has_header(self):
        rows = revenue_by_customer(seeded_db(), tenant_id=1)
        self.assertEqual(format_report(rows).splitlines()[0], "customer,orders,revenue")

    def test_report_returns_rows(self):
        rows = revenue_by_customer(seeded_db(), tenant_id=1)
        self.assertGreaterEqual(len(rows), 1)


if __name__ == "__main__":
    unittest.main()
