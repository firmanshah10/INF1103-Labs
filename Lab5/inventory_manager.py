import json

inventory = [{"id": 'P001','name':'Laptop','price':1000,'stock':40},{"id": 'P002','name':'Mouse','price':30,'stock':30},{"id": 'P003','name':'Keyboard','price':45,'stock':89}]

def load_inventory():
    try:
        with open('inventory.json', 'r') as file:
            print("inventory.json found.")
            data = json.load(file)
            print("Inventory loaded successfully.")
            return data
    except FileNotFoundError:
        print("inventory.json not found. Starting with default inventory.")
        # 3 default products
        return [
            {"id": "P001", "name": "Laptop", "price": 1000, "stock": 40},
            {"id": "P002", "name": "Mouse", "price": 30, "stock": 30},
            {"id": "P003", "name": "Keyboard", "price": 45, "stock": 89}
        ]
    def save_inventory():
        with open('inventory.json', 'w') as file:
            json.dump(inventory, file, indent=4)
    print("Inventory saved successfully to inventory.json.")

def display_all():
    for inv in inventory:
        print(f"ID: {inv['id']} | Name: {inv['name']} | Price: ${inv['price']} | Stock: {inv['stock']}")

def add_product():
    
    print("Add New Product\n")
    product_id = input(f"Product ID: ")
    product_name = input(f"Product Name: ")
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

def update_stock():
    print("Update Stock:  ")
    search_id = input("Enter Product ID:")
    for inv in inventory:
        if search_id == inv['id']:
            print("Product Found: ")
            print(f"Name: {inv['name']}")
            print(f"Current Stock: {inv['stock']}")
            while True:
                new_stock = input("New Stock Quantity: ")
                if new_stock.isdigit():
                    int_stock = int(new_stock)
                    break
                else:
                    print("Invalid quantity, please enter a number")
            inv['stock'] = int_stock
def search_product():
    print("Search Product")
    search_id = input("Enter Product ID: ")
    for inv in inventory:
        if search_id == inv['id']:
            print("Product Found")
            print("--------------------------")
            print(f"ID: {inv['id']}")
            print(f"Name: {inv['name']}")
            print(f"Price: {inv['price']}")
            print(f"Stock: {inv['stock']}")
            print("--------------------------")
            break
    else:
        print("Product not found")

search_product()
#update_stock()
#add_product()
#display_all()