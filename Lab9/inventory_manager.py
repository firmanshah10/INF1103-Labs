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
    """abstract base class for products with validation and supplier association"""

    def __init__(
        self,
        product_id: str,
        name: str,
        price: float,
        stock: int,
        supplier: Supplier,
    ):
        price_val = float(price)
        stock_val = int(stock)
        if price_val <= 0:
            raise ValueError("Price must be greater than zero.")
        if stock_val < 0:
            raise ValueError("Stock quantity cannot be negative.")

        self._product_id: str = product_id
        self.name: str = name
        self._price: float = price_val
        self._stock: int = stock_val
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
        new_stock = int(quantity)
        if new_stock < 0:
            raise ValueError("Stock quantity cannot be negative.")
        self._stock = new_stock

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
        qty = int(quantity)
        if qty <= 0:
            raise ValueError("Quantity must be greater than zero.")
        self.product: Product = product
        self.quantity: int = qty

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

class ProductFactory:
    """centralised factory for creating Product instances"""

    @staticmethod
    def create(
        product_type: str,
        product_id: str,
        name: str,
        price: float,
        stock_quantity: int,
        supplier: Supplier,
        extra_attr: float = 1.0,
    ) -> Product:
        normalized_type = product_type.strip().lower()
        if normalized_type == "physical":
            return PhysicalProduct(
                product_id, name, price, stock_quantity, supplier, extra_attr
            )
        if normalized_type == "digital":
            return DigitalProduct(
                product_id, name, price, stock_quantity, supplier, extra_attr
            )
        raise ValueError(f"Unknown product type: {product_type}")

def get_positive_float(prompt: str) -> float:
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Please enter a number greater than zero.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number, e.g. 12.50")


def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None:
    loaded = 0
    try:
        file = open(path, newline="", encoding="utf-8")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        with file:
            reader = csv.reader(file)
            header = next(reader, None)
            for row in reader:
                if not row or all(cell.strip() == "" for cell in row):
                    continue
                try:
                    if len(row) < 5:
                        raise ValueError("Row must contain 5 columns.")
                    p_type = row[0].strip()
                    p_id = row[1].strip()
                    p_name = row[2].strip()
                    price = float(row[3].strip())
                    stock = int(row[4].strip())
                    extra = float(row[5].strip()) if len(row) > 5 and row[5].strip() else 1.0
                    product = ProductFactory.create(
                        p_type, p_id, p_name, price, stock, supplier, extra
                    )
                    inventory.add_product(product)
                    loaded += 1
                except ValueError as exc:
                    print(f"Skipping invalid row {row}: {exc}")
        print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")


def load_inventory() -> Inventory:
    inv = Inventory()
    try:
        with open("inventory.json", "r", encoding="utf-8") as file:
            print("inventory.json found.")
            data = json.load(file)
            print("Inventory loaded successfully.")
            for item in data:
                sup_data = item.get(
                    "supplier",
                    {
                        "supplier_id": "S999",
                        "name": "Default Supplier",
                        "contact_email": "default@supp.com",
                    },
                )
                supplier = Supplier(
                    sup_data["supplier_id"],
                    sup_data["name"],
                    sup_data["contact_email"],
                )
                p_type = item.get("type", "")
                if p_type == "physical":
                    extra = item.get("weight", 1.0)
                elif p_type == "digital":
                    extra = item.get("download_size", 100.0)
                else:
                    continue
                try:
                    prod = ProductFactory.create(
                        p_type,
                        item["id"],
                        item["name"],
                        item["price"],
                        item["stock"],
                        supplier,
                        extra,
                    )
                    inv.add_product(prod)
                except ValueError as exc:
                    print(f"Skipping invalid saved item: {exc}")
            return inv
    except (FileNotFoundError, json.JSONDecodeError):
        print("inventory.json not found or corrupted. Starting with default inventory.")
        default_supplier = Supplier("S001", "TechCorp Global", "support@techcorp.com")
        default_items = [
            ProductFactory.create(
                "physical", "P001", "Gaming Laptop", 1200.00, 15, default_supplier, 2.5
            ),
            ProductFactory.create(
                "digital", "P002", "Antivirus Software", 25.50, 40, default_supplier, 500.0
            ),
            ProductFactory.create(
                "physical", "P003", "Mechanical Keyboard", 45.00, 25, default_supplier, 1.2
            ),
        ]
        for prod in default_items:
            inv.add_product(prod)
        return inv


def save_inventory(inventory: Inventory) -> None:
    data = [prod.to_dict() for prod in inventory.products]
    with open("inventory.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
    print("Inventory saved successfully to inventory.json.")


def main() -> None:
    print("==================================================")
    print("INVENTORY MANAGEMENT SYSTEM (LAB 9 - PATTERNS & ERRORS)")
    print("==================================================")
    inventory = load_inventory()

    if inventory.products:
        print("\n--- Testing Strategy & Order ---")
        sample_order = Order("ORD-1001", discount=BulkDiscount(200, 20))
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

        if choice == "1":
            inventory.display_all()
        elif choice == "2":
            print("\nAdd New Product\n")
            p_type = input("Product Type ('physical' or 'digital'): ").strip().lower()
            product_id = input("Product ID: ").strip()
            product_name = input("Product Name: ").strip()

            sup_id = input("Supplier ID: ").strip()
            sup_name = input("Supplier Name: ").strip()
            sup_email = input("Supplier Email: ").strip()
            supplier = Supplier(sup_id, sup_name, sup_email)

            float_price = get_positive_float("Price: ")
            while True:
                stock_quantity = input("Stock Quantity: ").strip()
                if stock_quantity.isdigit():
                    int_quantity = int(stock_quantity)
                    break
                print("Invalid quantity, please type a non-negative whole number.")

            if p_type == "physical":
                extra = get_positive_float("Weight (kg): ")
            elif p_type == "digital":
                extra = get_positive_float("Download Size (MB): ")
            else:
                print("Unknown type. Defaulting to physical with 1kg weight.")
                p_type = "physical"
                extra = 1.0

            try:
                new_product = ProductFactory.create(
                    p_type, product_id, product_name, float_price, int_quantity, supplier, extra
                )
                inventory.add_product(new_product)
                print("Product added successfully!")
            except ValueError as exc:
                print(f"Could not create product: {exc}")

        elif choice == "3":
            print("\nUpdate Stock")
            search_id = input("Enter Product ID: ").strip()
            prod = inventory.find_product(search_id)
            if prod:
                print(f"\nProduct Found: {prod.name} (Current Stock: {prod.stock})")
                while True:
                    new_stock = input("New Stock Quantity: ").strip()
                    if new_stock.isdigit():
                        try:
                            prod.update_stock(int(new_stock))
                            print("\nStock updated successfully!")
                            break
                        except ValueError as exc:
                            print(exc)
                    else:
                        print("Invalid quantity, please enter a non-negative whole number.")
            else:
                print("Product not found.")

        elif choice == "4":
            print("\nSearch Product")
            search_id = input("Enter Product ID: ").strip()
            prod = inventory.find_product(search_id)
            if prod:
                print("\nProduct Found:")
                print(
                    "--------------------------------------------------------------------------------"
                )
                prod.display_information()
                print(
                    "\n--------------------------------------------------------------------------------"
                )
            else:
                print("\nProduct not found.")

        elif choice == "5":
            print("Saving inventory...")
            save_inventory(inventory)

        elif choice == "6":
            print("\nSaving inventory before exit...")
            save_inventory(inventory)
            print("\nThank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option, please choose between 1 and 6.")


if __name__ == "__main__":
    main()