import io
import os
import tempfile
import unittest
from unittest.mock import patch

from inventory_manager import (
    BulkDiscount,
    DigitalProduct,
    Inventory,
    NoDiscount,
    Order,
    OrderLine,
    PercentageDiscount,
    PhysicalProduct,
    ProductFactory,
    StudentDiscount,
    Supplier,
    get_positive_float,
    load_products,
)


class TestLab9(unittest.TestCase):
    def setUp(self) -> None:
        self.supplier = Supplier("S001", "Acme Supplies", "acme@example.com")
        self.physical = ProductFactory.create(
            "physical", "P10", "Desk", 100.0, 5, self.supplier, 2.0
        )
        self.digital = ProductFactory.create(
            "digital", "D10", "E-Book", 150.0, 20, self.supplier, 120.0
        )

    def test_discount_strategies_and_set_discount(self) -> None:
        order = Order("O1")
        self.assertIsInstance(order.discount, NoDiscount)
        order.add_order_line(self.physical, 1)  # 100
        order.add_order_line(self.digital, 1)   # 150 -> total 250

        order.set_discount(BulkDiscount(200, 20))
        self.assertAlmostEqual(order.calculate_total(), 230.0)

        order.set_discount(PercentageDiscount(10))
        self.assertAlmostEqual(order.calculate_total(), 225.0)

        order.set_discount(StudentDiscount(5))
        self.assertAlmostEqual(order.calculate_total(), 237.5)

    def test_factory_creates_subclasses_and_rejects_unknown_type(self) -> None:
        self.assertIsInstance(self.physical, PhysicalProduct)
        self.assertIsInstance(self.digital, DigitalProduct)
        with self.assertRaises(ValueError):
            ProductFactory.create(
                "service", "SV1", "Install", 30.0, 2, self.supplier
            )

    def test_validation_rules(self) -> None:
        with self.assertRaises(ValueError):
            ProductFactory.create("physical", "P11", "Bad Price", 0.0, 2, self.supplier)
        with self.assertRaises(ValueError):
            ProductFactory.create("physical", "P12", "Neg Stock", 10.0, -1, self.supplier)
        with self.assertRaises(ValueError):
            OrderLine(self.physical, 0)
        with self.assertRaises(ValueError):
            self.physical.update_stock(-3)

    def test_get_positive_float_handles_invalid_inputs(self) -> None:
        with patch("builtins.input", side_effect=["abc", "-5", "12.50"]):
            with patch("sys.stdout", new=io.StringIO()):
                result = get_positive_float("Price: ")
        self.assertAlmostEqual(result, 12.50)

    def test_load_products_handles_bad_rows_and_missing_file(self) -> None:
        inv = Inventory()
        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = os.path.join(tmpdir, "products.csv")
            with open(csv_path, "w", encoding="utf-8") as f:
                f.write("product_type,product_id,name,price,stock_quantity\n")
                f.write("physical,P001,Desk Lamp,25.00,10\n")
                f.write("digital,D001,Photo Editor,49.90,100\n")
                f.write("service,S001,Installation,30.00,5\n")
                f.write("physical,P002,Office Chair,abc,3\n")
                f.write("physical,P003,Monitor Stand,39.50,7\n")

            buf = io.StringIO()
            with patch("sys.stdout", new=buf):
                load_products(csv_path, inv, self.supplier)
            out = buf.getvalue()
            self.assertEqual(len(inv.products), 3)
            self.assertIn("3 products loaded.", out)
            self.assertIn("Load attempt finished.", out)

            missing_buf = io.StringIO()
            with patch("sys.stdout", new=missing_buf):
                load_products(os.path.join(tmpdir, "missing.csv"), inv, self.supplier)
            m_out = missing_buf.getvalue()
            self.assertIn("Products file not found:", m_out)
            self.assertIn("Load attempt finished.", m_out)


if __name__ == "__main__":
    unittest.main()