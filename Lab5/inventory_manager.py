inventory = [{"id": 'P001','name':'Laptop','price':1000,'stock':40},{"id": 'P002','name':'Mouse','price':30,'stock':30},{"id": 'P003','name':'Keyboard','price':45,'stock':89}]

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

add_product()
display_all()