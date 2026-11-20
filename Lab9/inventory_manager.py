import csv
import json
from abc import ABC, abstractmethod
from typing import Optional


class CanBeShipped(ABC):
    """interface contract for shippable items"""

    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        pass


class Supplier:
    """"represents a supplier associated with a product"""

    def __init__(self, supplier_id: str, name: str, contact_email: str):
        self.supplier_id: str = supplier_id
        self.name: str = name
        self.contact_email: str = contact_email

    def display_information(self) -> None:
        print(
            f"Supplier ID: {self.supplier_id} | Name: {self.name} | Email: {self.contact_email}"
        )


class Product(ABC):
    """abstract base class for products with supplier association"""

    def __init__(
        self,
        product_id: str,
        name: str,
        price: float,
        stock: int,
        supplier: Supplier,
    ):
        self._product_id: str = product_id
        self.name: str = name
        self._price: float = float(price)
        self._stock: int = int(stock)
        self.supplier: Supplier = supplier

    @property
    def product_id(self) -> str:
        return self._product_id

    @property
    def price(self) -> float:
        return self._price

    @property
    def stock(self) -> int:
        return self._stock

    def update_stock(self, quantity: int) -> None:
        self._stock = int(quantity)

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        pass

    def display_information(self) -> None:
        print(
            f"ID: {self._product_id} | Name: {self.name} | Price: ${self._price:.2f} "
            f"| Stock: {self._stock} | Supplier: {self.supplier.name}",
            end="",
        )

    def to_dict(self) -> dict:
        return {
            "id": self._product_id,
            "name": self.name,
            "price": self._price,
            "stock": self._stock,
            "supplier": {
                "supplier_id": self.supplier.supplier_id,
                "name": self.supplier.name,
                "contact_email": self.supplier.contact_email,
            },
        }


class PhysicalProduct(Product, CanBeShipped):
    """subclass representing a physical product"""

    def __init__(
        self,
        product_id: str,
        name: str,
        price: float,
        stock: int,
        supplier: Supplier,
        weight: float,
    ):
        super().__init__(product_id, name, price, stock, supplier)
        self._weight: float = float(weight)

    @property
    def weight(self) -> float:
        return self._weight

    def get_fulfilment_info(self) -> str:
        return "Product requires physical shipping."

    def calculate_shipping_cost(self) -> float:
        return 5.0 + (self._weight * 2.0)

    def display_information(self) -> None:
        super().display_information()
        print(
            f" | Type: Physical | Weight: {self._weight}kg "
            f"| Shipping: ${self.calculate_shipping_cost():.2f} "
            f"| Fulfilment: {self.get_fulfilment_info()}"
        )

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["type"] = "physical"
        data["weight"] = self._weight
        return data


class DigitalProduct(Product):
    """subclass representing a digital product"""

    def __init__(
        self,
        product_id: str,
        name: str,
        price: float,
        stock: int,
        supplier: Supplier,
        download_size: float,
    ):
        super().__init__(product_id, name, price, stock, supplier)
        self._download_size: float = float(download_size)

    @property
    def download_size(self) -> float:
        return self._download_size

    def get_fulfilment_info(self) -> str:
        return "Product is delivered digitally via download link."

    def display_information(self) -> None:
        super().display_information()
        print(
            f" | Type: Digital | Download Size: {self._download_size}MB "
            f"| Fulfilment: {self.get_fulfilment_info()}"
        )

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["type"] = "digital"
        data["download_size"] = self._download_size
        return data


class DiscountStrategy(ABC):
    """abstract strategy interface for order discounts"""

    @abstractmethod
    def apply(self, total: float) -> float:
        pass


class NoDiscount(DiscountStrategy):
    """strategy that applies no discount"""

    def apply(self, total: float) -> float:
        return float(total)


class PercentageDiscount(DiscountStrategy):
    """strategy that applies a percentage discount"""

    def __init__(self, percentage: float):
        self.percentage: float = float(percentage)

    def apply(self, total: float) -> float:
        return float(total) * (1.0 - self.percentage / 100.0)


class BulkDiscount(DiscountStrategy):
    """strategy that subtracts an amount when total meets a minimum threshold"""

    def __init__(self, threshold: float, discount_amount: float):
        self.threshold: float = float(threshold)
        self.discount_amount: float = float(discount_amount)

    def apply(self, total: float) -> float:
        if total >= self.threshold:
            return float(total) - self.discount_amount
        return float(total)


class StudentDiscount(DiscountStrategy):
    """strategy that applies a 5% student discount"""

    def __init__(self, percentage: float = 5.0):
        self.percentage: float = float(percentage)

    def apply(self, total: float) -> float:
        return float(total) * (1.0 - self.percentage / 100.0)


class OrderLine:
    """order line item representing product and quantity"""

    def __init__(self, product: Product, quantity: int):
        self.product: Product = product
        self.quantity: int = int(quantity)

    def calculate_subtotal(self) -> float:
        return self.product.price * self.quantity

    def display_order_line(self) -> None:
        print(
            f"  - {self.product.name} x {self.quantity} @ ${self.product.price:.2f} "
            f"each = Subtotal: ${self.calculate_subtotal():.2f}"
        )


class Order:
    """customer order containing OrderLine items and a DiscountStrategy"""

    def __init__(
        self,
        order_id: str,
        discount: Optional[DiscountStrategy] = None,
    ):
        self.order_id: str = order_id
        self.order_lines: list[OrderLine] = []
        self.discount: DiscountStrategy = (
            discount if discount is not None else NoDiscount()
        )

    def set_discount(self, strategy: DiscountStrategy) -> None:
        self.discount = strategy

    def add_order_line(self, product: Product, quantity: int) -> None:
        order_line = OrderLine(product, quantity)
        self.order_lines.append(order_line)

    def calculate_total(self) -> float:
        total = sum(line.calculate_subtotal() for line in self.order_lines)
        return self.discount.apply(total)

    def display_order(self) -> None:
        print(f"\nOrder ID: {self.order_id}")
        for line in self.order_lines:
            line.display_order_line()
        print(f"Total Order Value: ${self.calculate_total():.2f}")


class Inventory:
    """manages a collection of Product objects (Aggregation)"""

    def __init__(self):
        self.products: list[Product] = []

    def add_product(self, product: Product) -> None:
        self.products.append(product)

    def remove_product(self, product_id: str) -> None:
        self.products = [p for p in self.products if p.product_id != product_id]

    def find_product(self, product_id: str) -> Optional[Product]:
        for prod in self.products:
            if prod.product_id == product_id:
                return prod
        return None

    def display_all(self) -> None:
        if not self.products:
            print("\nInventory is empty.")
            return
        print(
            "--------------------------------------------------------------------------------"
        )
        print("\nCurrent Inventory")
        print(
            "--------------------------------------------------------------------------------"
        )
        for prod in self.products:
            prod.display_information()
            print(f"  -> Fulfilment Test: {prod.get_fulfilment_info()}")