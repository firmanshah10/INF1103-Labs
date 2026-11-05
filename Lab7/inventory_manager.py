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