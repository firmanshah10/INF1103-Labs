import json

def load_inventory():
    try:
        with open('inventory.json', 'r') as file:
            print("inventory.json found.")
            data = json.load(file)
            print("Inventory loaded successfully.")
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        print("inventory.json not found. Starting with default inventory.")
        # 3 default products
        return [
            {"id": "P001", "name": "Laptop", "price": 1200.00, "stock": 15},
            {"id": "P002", "name": "Mouse", "price": 25.50, "stock": 40},
            {"id": "P003", "name": "Keyboard", "price": 45.00, "stock": 25}
        ]
def save_inventory(inventory):
    with open('inventory.json', 'w') as file:
        json.dump(inventory, file, indent=4)
    print("Inventory saved successfully to inventory.json.")

def display_all(inventory):
    print("------------------------------")
    print("\nCurrent Inventory")
    print("------------------------------")
    for inv in inventory:
        print(f"ID: {inv['id']} | Name: {inv['name']} | Price: ${inv['price']:.2f} | Stock: {inv['stock']}")

def add_product(inventory):
    
    print("Add New Product\n")
    product_id = input(f"Product ID: ").strip()
    product_name = input(f"Product Name: ").strip()
    while True:

        product_price = input(f"Price: ")
        try:
             float_price= float(product_price)
             break
        except ValueError:
            print("Invalid price, please type a number: ")
    while True:
        stock_quantity = input(f"Stock Quantity: ")
        if stock_quantity.isdigit():
            int_quantity = int(stock_quantity)
            break
        else:
            print("Invalid quantity, please type a number")
    new_product = {"id":product_id, "name": product_name, "price":float_price, "stock":int_quantity}
    inventory.append(new_product)
    print("Product added successfully!")

def update_stock(inventory):
    print("\nUpdate Stock")
    search_id = input("Enter Product ID: ").strip()
    for inv in inventory:
        if search_id == inv['id']:
            print("\nProduct Found:")
            print(f"Name: {inv['name']}")
            print(f"Current Stock: {inv['stock']}\n")
            while True:
                new_stock = input("New Stock Quantity: ")
                if new_stock.isdigit():
                    inv['stock'] = int(new_stock)
                    print("\nStock updated successfully!")
                    break
                else:
                    print("Invalid quantity, please enter a number")
            break
    else:
        print("Product not found.")
def search_product(inventory):
    print("Search Product")
    search_id = input("Enter Product ID: ")
    for inv in inventory:
        if search_id == inv['id']:
            print("\nProduct Found")
            print("--------------------------")
            print(f"ID: {inv['id']}")
            print(f"Name: {inv['name']}")
            print(f"Price: {inv['price']:.2f}")
            print(f"Stock: {inv['stock']}")
            print("--------------------------")
            break
    else:
        print("\nProduct not found")

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
            display_all(inventory)
        elif choice == '2':
            add_product(inventory)
        elif choice == '3':
            update_stock(inventory)
        elif choice == '4':
            search_product(inventory)
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