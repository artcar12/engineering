import unittest

from app.orders import subtotal_cents, total_cents


class OrderTotals(unittest.TestCase):
    def test_subtotal_sums_lines(self):
        order = {"lines": [{"unit_cents": 500, "quantity": 2}, {"unit_cents": 100, "quantity": 1}]}
        self.assertEqual(subtotal_cents(order), 1100)

    def test_total_without_discount_equals_subtotal(self):
        order = {"lines": [{"unit_cents": 500, "quantity": 2}]}
        self.assertEqual(total_cents(order), 1000)

    def test_discount_is_subtracted(self):
        order = {"lines": [{"unit_cents": 500, "quantity": 2}], "discount_cents": 300}
        self.assertEqual(total_cents(order), 700)

    def test_total_never_negative(self):
        order = {"lines": [{"unit_cents": 100, "quantity": 1}], "discount_cents": 500}
        self.assertEqual(total_cents(order), 0)


if __name__ == "__main__":
    unittest.main()
