class Product:
    """store product info"""
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
        """update stock quantity"""
        self._stock = int(quantity)

    def display_information(self):
        """display info"""
        print(f"ID: {self._product_id} | Name: {self.name} | Price: ${self._price:.2f} | Stock: {self._stock}")

    def to_dict(self):
        """convert product object into dict for json"""
        return {
            "id": self._product_id,
            "name": self.name,
            "price": self._price,
            "stock": self._stock
        }

class Inventory:
    """store and manage the products"""
    def __init__(self):
        self.products = []

    def add_product(self, product):
        """add a product object to inventory"""
        self.products.append(product)

    def search_product(self, product_id):
        """search for product by id and returns the product object if found"""
        for prod in self.products:
            if prod.product_id == product_id:
                return prod
        return None

    def display_all(self):
        """display all products in inventory"""
        if not self.products:
            print("\nInventory is empty.")
            return
        print("------------------------------")
        print("\nCurrent Inventory")
        print("------------------------------")
        for prod in self.products:
            prod.display_information()