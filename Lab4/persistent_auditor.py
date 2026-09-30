def get_valid_input():
    failed = 0
    name = input('Enter Product Name: ')
    if name == 'quit':
        return('quit', None), failed
    while True:
        entry = input("Enter a stock quantity (or quit): ")
        if entry == "quit":
            return "quit", failed
        if entry.isdigit():
            return (name,int(entry)), failed
        else:
            print("Invalid input, please enter a valid input")
            failed += 1

def process_delivery(total, result):
    new_total = total + result
    return new_total

def calculate_tax(amount):
    tax = amount * 0.1
    return tax

def generate_report(process_delivery,total_unit,failed_attemps):
    print(f'Total Transactions Recorded: {total_unit}')
    print(f'Total Deliveries Processed: {process_delivery}')
    print(f'Number of Failed Entries: {failed_attemps}')

def load_inventory():
    orders = []
    try:
        with open('inventory.txt', 'r') as file:
            print('Current Orders: ')
            for line in file:
                line = line.strip()
                if line:
                    print(line)
                    orders.append(line.split(', '))
    except FileNotFoundError:
        print('File not found')
    return orders

def save_inventory(orders):
    with open('inventory.txt', 'w') as file:
        for order in orders:
            file.write(f'{order[0]}, {order[1]}, {order[2]}\n')
    print(f'Order successfully added to inventory.txt')

orders = load_inventory()
total = 0
deliveries = 0
rejected = 0

while True:
    (item_info), failed = get_valid_input()
    rejected += failed
    
    if item_info[0] == "quit":
        break
        
    product_name, quantity = item_info
    next_id = 1001 + len(orders)
    
    new_order = [str(next_id), product_name, str(quantity)]
    orders.append(new_order)
    
    print("\nNew Order Added:")
    print(f"{new_order[0]}, {new_order[1]}, {new_order[2]}")
    
    save_inventory(orders)
    
    total = process_delivery(total, quantity)
    tax = calculate_tax(quantity)
    deliveries += 1

generate_report(deliveries, total, rejected)

