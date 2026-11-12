import json
from abc import ABC, abstractmethod

class CanBeShipped(ABC):
    """interface contract"""
    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        pass

class Supplier:
    """supplier associated with a product"""
    def __init__(self, supplier_id: str, name: str, contact_email: str):
        self.supplier_id: str = supplier_id
        self.name: str = name
        self.contact_email: str = contact_email

    def display_information(self) -> None:
        print(f"Supplier ID: {self.supplier_id} | Name: {self.name} | Email: {self.contact_email}")

class Product(ABC):
    """abstract base class"""
    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier):
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
        print(f"ID: {self._product_id} | Name: {self.name} | Price: ${self._price:.2f} | Stock: {self._stock} | Supplier: {self.supplier.name}", end="")

    def to_dict(self) -> dict:
        return {
            "id": self._product_id,
            "name": self.name,
            "price": self._price,
            "stock": self._stock,
            "supplier": {
                "supplier_id": self.supplier.supplier_id,
                "name": self.supplier.name,
                "contact_email": self.supplier.contact_email
            }
        }

class PhysicalProduct(Product, CanBeShipped):
    """subclass representing a physical product"""
    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier, weight: float):
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
        print(f" | Type: Physical | Weight: {self._weight}kg | Shipping: ${self.calculate_shipping_cost():.2f} | Fulfilment: {self.get_fulfilment_info()}")

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["type"] = "physical"
        data["weight"] = self._weight
        return data

class DigitalProduct(Product):
    """subclass representing a digital product"""
    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier, download_size: float):
        super().__init__(product_id, name, price, stock, supplier)
        self._download_size: float = float(download_size)

    @property
    def download_size(self) -> float:
        return self._download_size

    def get_fulfilment_info(self) -> str:
        return "Product is delivered digitally via download link."

    def display_information(self) -> None:
        super().display_information()
        print(f" | Type: Digital | Download Size: {self._download_size}MB | Fulfilment: {self.get_fulfilment_info()}")

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["type"] = "digital"
        data["download_size"] = self._download_size
        return data