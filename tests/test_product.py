import unittest
from models.product import Product


class TestProduct(unittest.TestCase):
    def test_total_price_non_weighed(self):
        """Для невзвешиваемого товара total_price() должен возвращать просто price."""
        p = Product(name="Шоколадка", price=50.0, needs_weighing=False, stock=10)
        self.assertEqual(p.total_price(), 50.0)

    def test_total_price_weighed_without_weight_raises(self):
        """Для взвешиваемого товара, если weight == None, total_price() бросит ValueError."""
        p = Product(name="Говядина", price=800.0, needs_weighing=True, stock=100)
        with self.assertRaises(ValueError) as cm:
            _ = p.total_price()
        self.assertIn("должен быть взвешен", str(cm.exception))

    def test_weigh_and_total_price(self):
        """После вызова p.weigh(x) total_price() == price * weight."""
        p = Product(name="Яблоки", price=100.0, needs_weighing=True, stock=50)
        p.weigh(2.5)
        expected = 100.0 * 2.5
        self.assertAlmostEqual(p.total_price(), expected)


if __name__ == "__main__":
    unittest.main()
