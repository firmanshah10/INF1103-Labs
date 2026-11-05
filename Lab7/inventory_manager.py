import json
from abc import ABC, abstractmethod

class canbeshipped(ABC):
    """interface contract"""
    @abstractmethod
    def calculate_shipping_cost(self):
        pass

class product(ABC):
    def __init__(self, product_id, name, price, stock):
        self._product_id = product_id
        self.name = name
        self._price = float(price)
        self._stock = int(stock)

    @property
    def product_id(self):
        return self._product_id

    @property
    def price(self):
        return self._price

    @property
    def stock(self):
        return self._stock

    def update_stock(self, quantity):
        self._stock = int(quantity)

    @abstractmethod
    def get_fulfilment_info(self):
        pass

    def display_information(self):
        print(f"ID: {self._product_id} | Name: {self.name} | Price: ${self._price:.2f} | Stock: {self._stock}", end="")

    def to_dict(self):
        return {
            "id": self._product_id,
            "name": self.name,
            "price": self._price,
            "stock": self._stock
        }

class physicalproduct(product, canbeshipped):
    """subclass representing a physical product"""
    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)
        self._weight = float(weight)

    @property
    def weight(self):
        return self._weight

    def get_fulfilment_info(self):
        return "Product requires physical shipping."

    def calculate_shipping_cost(self):
        return 5.0 + (self._weight * 2.0)

    def display_information(self):
        super().display_information()
        print(f" | Type: Physical | Weight: {self._weight}kg | Shipping: ${self.calculate_shipping_cost():.2f} | Fulfilment: {self.get_fulfilment_info()}")

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "physical"
        data["weight"] = self._weight
        return data

class digitalproduct(product):
    """subclass representing a digital product"""
    def __init__(self, product_id, name, price, stock, download_size):
        super().__init__(product_id, name, price, stock)
        self._download_size = float(download_size)

    @property
    def download_size(self):
        return self._download_size

    def get_fulfilment_info(self):
        return "Product is delivered digitally via download link."

    def display_information(self):
        super().display_information()
        print(f" | Type: Digital | Download Size: {self._download_size}MB | Fulfilment: {self.get_fulfilment_info()}")

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "digital"
        data["download_size"] = self._download_size
        return data