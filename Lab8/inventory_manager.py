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

class OrderLine:
    """order line item"""
    def __init__(self, product: Product, quantity: int):
        self.product: Product = product
        self.quantity: int = int(quantity)

    def calculate_subtotal(self) -> float:
        return self.product.price * self.quantity

    def display_order_line(self) -> None:
        print(f"  - {self.product.name} x {self.quantity} @ ${self.product.price:.2f} each = Subtotal: ${self.calculate_subtotal():.2f}")

class Order:
    """customer order containing order lines"""
    def __init__(self, order_id: str):
        self.order_id: str = order_id
        self.order_lines: list[OrderLine] = []

    def add_order_line(self, product: Product, quantity: int) -> None:
        order_line = OrderLine(product, quantity)
        self.order_lines.append(order_line)

    def calculate_total(self) -> float:
        return sum(line.calculate_subtotal() for line in self.order_lines)

    def display_order(self) -> None:
        print(f"\nOrder ID: {self.order_id}")
        for line in self.order_lines:
            line.display_order_line()
        print(f"Total Order Value: ${self.calculate_total():.2f}")

class Inventory:
    """manage collection of Product objects"""
    def __init__(self):
        self.products: list[Product] = []

    def add_product(self, product: Product) -> None:
        self.products.append(product)

    def remove_product(self, product_id: str) -> None:
        self.products = [p for p in self.products if p.product_id != product_id]

    def find_product(self, product_id: str) -> Product | None:
        for prod in self.products:
            if prod.product_id == product_id:
                return prod
        return None

    def display_all(self) -> None:
        if not self.products:
            print("\nInventory is empty.")
            return
        print("--------------------------------------------------------------------------------")
        print("\nCurrent Inventory")
        print("--------------------------------------------------------------------------------")
        for prod in self.products:
            prod.display_information()
            print(f"  -> Fulfilment Test: {prod.get_fulfilment_info()}")

def load_inventory() -> Inventory:
    inv = Inventory()
    try:
        with open('inventory.json', 'r') as file:
            print("inventory.json found.")
            data = json.load(file)
            print("Inventory loaded successfully.")
            for item in data:
                sup_data = item.get("supplier", {"supplier_id": "S999", "name": "Default Supplier", "contact_email": "default@supp.com"})
                supplier = Supplier(sup_data["supplier_id"], sup_data["name"], sup_data["contact_email"])
                
                if item.get("type") == "physical":
                    prod = PhysicalProduct(item['id'], item['name'], item['price'], item['stock'], supplier, item['weight'])
                elif item.get("type") == "digital":
                    prod = DigitalProduct(item['id'], item['name'], item['price'], item['stock'], supplier, item['download_size'])
                else:
                    continue
                inv.add_product(prod)
            return inv
    except (FileNotFoundError, json.JSONDecodeError):
        print("inventory.json not found or corrupted. Starting with default inventory.")
        default_supplier = Supplier("S001", "TechCorp Global", "support@techcorp.com")
        default_items = [
            PhysicalProduct("P001", "Gaming Laptop", 1200.00, 15, default_supplier, 2.5),
            DigitalProduct("P002", "Antivirus Software", 25.50, 40, default_supplier, 500.0),
            PhysicalProduct("P003", "Mechanical Keyboard", 45.00, 25, default_supplier, 1.2)
        ]
        for prod in default_items:
            inv.add_product(prod)
        return inv

def save_inventory(inventory: Inventory) -> None:
    data = [prod.to_dict() for prod in inventory.products]
    with open('inventory.json', 'w') as file:
        json.dump(data, file, indent=4)
    print("Inventory saved successfully to inventory.json.")

def main() -> None:
    print("==================================================")
    print("INVENTORY MANAGEMENT SYSTEM (LAB 8 - RELATIONS)")
    print("==================================================")
    inventory = load_inventory()

    if inventory.products:
        print("\n--- Testing Composition (Order & OrderLine) ---")
        sample_order = Order("ORD-1001")
        sample_order.add_order_line(inventory.products[0], 2)
        if len(inventory.products) > 1:
            sample_order.add_order_line(inventory.products[1], 1)
        sample_order.display_order()

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
            
            sup_id = input("Supplier ID: ").strip()
            sup_name = input("Supplier Name: ").strip()
            sup_email = input("Supplier Email: ").strip()
            supplier = Supplier(sup_id, sup_name, sup_email)

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
                new_product = PhysicalProduct(product_id, product_name, float_price, int_quantity, supplier, weight)
            elif p_type == 'digital':
                while True:
                    try:
                        download_size = float(input("Download Size (MB): "))
                        break
                    except ValueError:
                        print("Invalid size, enter a number.")
                new_product = DigitalProduct(product_id, product_name, float_price, int_quantity, supplier, download_size)
            else:
                print("Unknown type. Defaulting to physical with 1kg weight.")
                new_product = PhysicalProduct(product_id, product_name, float_price, int_quantity, supplier, 1.0)

            inventory.add_product(new_product)
            print("Product added successfully!")

        elif choice == '3':
            print("\nUpdate Stock")
            search_id = input("Enter Product ID: ").strip()
            prod = inventory.find_product(search_id)
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
            prod = inventory.find_product(search_id)
            if prod:
                print("\nProduct Found:")
                print("--------------------------------------------------------------------------------")
                prod.display_information()
                print("\n--------------------------------------------------------------------------------")
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