import json
from abc import ABC, abstractmethod

class CanBeShipped(ABC):
    """interface contract"""
    @abstractmethod
    def calculate_shipping_cost(self):
        pass

class Product(ABC):
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

class PhysicalProduct(Product, CanBeShipped):
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

class DigitalProduct(Product):
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

class Inventory:
    """manage the collection of prod objects"""
    def __init__(self):
        self.products = []

    def add_product(self, product):
        self.products.append(product)

    def search_product(self, product_id):
        for prod in self.products:
            if prod.product_id == product_id:
                return prod
        return None

    def display_all(self):
        if not self.products:
            print("\nInventory is empty.")
            return
        print("--------------------------------------------------------------------------------")
        print("\nCurrent Inventory")
        print("--------------------------------------------------------------------------------")
        for prod in self.products:
            prod.display_information()

def load_inventory():
    """Loads inventory and recreates the correct subclasses based on JSON type identifiers."""
    inv = Inventory()
    try:
        with open('inventory.json', 'r') as file:
            print("inventory.json found.")
            data = json.load(file)
            print("Inventory loaded successfully.")
            for item in data:
                if item.get("type") == "physical":
                    prod = PhysicalProduct(item['id'], item['name'], item['price'], item['stock'], item['weight'])
                elif item.get("type") == "digital":
                    prod = DigitalProduct(item['id'], item['name'], item['price'], item['stock'], item['download_size'])
                else:
                    continue
                inv.add_product(prod) 
            return inv  
    except (FileNotFoundError, json.JSONDecodeError):
        print("inventory.json not found or corrupted. Starting with default inventory.")
        default_items = [
            PhysicalProduct("P001", "Laptop", 1200.00, 15, 2.5),
            DigitalProduct("P002", "Online PDF Course", 69.67, 999, 500.0),
            PhysicalProduct("P003", "Mechanical Keyboard", 45.00, 25, 1.2)
        ]
        for prod in default_items:
            inv.add_product(prod)
        return inv 

def save_inventory(inventory):
    data = [prod.to_dict() for prod in inventory.products]
    with open('inventory.json', 'w') as file:
        json.dump(data, file, indent=4)
    print("Inventory saved successfully to inventory.json.")

def main():
    print("===================================")
    print("INVENTORY MANAGEMENT SYSTEM")
    print("===================================")
    inventory = load_inventory()

    while True:
        print("\n-------- MENU --------")
        print("1. Display All Products")
        print("2. Add Product")
        print("3. Update Stock")
        print("4. Search Product")
        print("5. Save Inventory")
        print("6. Exit")

        choice = input("Enter option: ").strip()

        if choice == '1':
            inventory.display_all()
        elif choice == '2':
            print("\nAdd New Product\n")
            p_type = input("Product Type ('physical' or 'digital'): ").strip().lower()
            product_id = input("Product ID: ").strip()
            product_name = input("Product Name: ").strip()
            while True:
                product_price = input("Price: ")
                try:
                    float_price = float(product_price)
                    break
                except ValueError:
                    print("Invalid price, please type a number: ")
            while True:
                stock_quantity = input("Stock Quantity: ")
                if stock_quantity.isdigit():
                    int_quantity = int(stock_quantity)
                    break
                else:
                    print("Invalid quantity, please type a number")
            
            if p_type == 'physical':
                while True:
                    try:
                        weight = float(input("Weight (kg): "))
                        break
                    except ValueError:
                        print("Invalid weight, enter a number.")
                new_product = PhysicalProduct(product_id, product_name, float_price, int_quantity, weight)
            elif p_type == 'digital':
                while True:
                    try:
                        download_size = float(input("Download Size (MB): "))
                        break
                    except ValueError:
                        print("Invalid size, enter a number.")
                new_product = DigitalProduct(product_id, product_name, float_price, int_quantity, download_size)
            else:
                print("Unknown type. Defaulting to physical with 1kg weight.")
                new_product = PhysicalProduct(product_id, product_name, float_price, int_quantity, 1.0)

            inventory.add_product(new_product)
            print("Product added successfully!")

        elif choice == '3':
            print("\nUpdate Stock")
            search_id = input("Enter Product ID: ").strip()
            prod = inventory.search_product(search_id)
            if prod:
                print(f"\nProduct Found: {prod.name} (Current Stock: {prod.stock})")
                while True:
                    new_stock = input("New Stock Quantity: ")
                    if new_stock.isdigit():
                        prod.update_stock(int(new_stock))
                        print("\nStock updated successfully!")
                        break
                    else:
                        print("Invalid quantity, please enter a number")
            else:
                print("Product not found.")

        elif choice == '4':
            print("\nSearch Product")
            search_id = input("Enter Product ID: ").strip()
            prod = inventory.search_product(search_id)
            if prod:
                print("\nProduct Found:")
                print("--------------------------------------------------------------------------------")
                prod.display_information()
                print("--------------------------------------------------------------------------------")
            else:
                print("\nProduct not found.")

        elif choice == '5':
            print("Saving inventory...")
            save_inventory(inventory)

        elif choice == '6':
            print("\nSaving inventory before exit...")
            save_inventory(inventory)
            print("\nThank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option, please choose between 1 and 6.")

if __name__ == "__main__":
    main()