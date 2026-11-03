import json

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

def load_inventory():
    """load inventory data from json and initialise"""
    inventory = Inventory()
    try:
        with open('inventory.json', 'r') as file:
            print("inventory.json found.")
            data = json.load(file)
            print("Inventory loaded successfully.")
            for item in data:
                prod = Product(item['id'], item['name'], item['price'], item['stock'])
                inventory.add_product(prod)
            return inventory
    except (FileNotFoundError, json.JSONDecodeError):
        print("inventory.json not found or corrupted. Starting with default inventory.")
        default_items = [
            Product("P001", "Laptop", 1200.00, 15),
            Product("P002", "Mouse", 25.50, 40),
            Product("P003", "Keyboard", 45.00, 25)
        ]
        for prod in default_items:
            inventory.add_product(prod)
        return inventory

def save_inventory(inventory):
    """saves inventory as dictionary to json"""
    data = [prod.to_dict() for prod in inventory.products]
    with open('inventory.json', 'w') as file:
        json.dump(data, file, indent=4)
    print("Inventory saved successfully to inventory.json.")

def main():
    print("===================================")
    print("INVENTORY MANAGEMENT SYSTEM (OOP)")
    print("===================================")
    inventory = Inventory()
    
    #default products using product class
    inventory.add_product(Product("P001", "Laptop", 1200.00, 15))
    inventory.add_product(Product("P002", "Mouse", 25.50, 40))
    inventory.add_product(Product("P003", "Keyboard", 45.00, 25))

    while True:
        print("\n-------- MENU --------")
        print("1. Display All Products")
        print("2. Add Product")
        print("3. Update Stock")
        print("4. Search Product")
        print("5. Exit")

        choice = input("Enter option: ").strip()

        if choice == '1':
            inventory.display_all()
        elif choice == '2':
            print("\nAdd New Product\n")
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
            
            new_product = Product(product_id, product_name, float_price, int_quantity)
            inventory.add_product(new_product)
            print("Product added successfully!")

        elif choice == '3':
            print("\nUpdate Stock")
            search_id = input("Enter Product ID: ").strip()
            prod = inventory.search_product(search_id)
            if prod:
                print("\nProduct Found:")
                print(f"Name: {prod.name}")
                print(f"Current Stock: {prod.stock}\n")
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
                print("\nProduct Found")
                print("--------------------------")
                prod.display_information()
                print("--------------------------")
            else:
                print("\nProduct not found.")

        elif choice == '5':
            print("\nThank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option, please choose between 1 and 5.")

if __name__ == "__main__":
    main()