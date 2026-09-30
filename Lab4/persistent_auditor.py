def get_valid_input():
    failed = 0
    while True:
        entry = input("Enter a stock quantity (or quit): ")
        if entry == "quit":
            return "quit", failed
        if entry.isdigit():
            return int(entry), failed
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
        print('File not found, creating new Inventory file...')
    return orders

def save_inventory():
    with open('inventorhy.txt', 'w') as file:
        data = file.write()


total = 0
deliveries = 0
rejected = 0

while True:
    result, failed = get_valid_input()
    rejected+= failed
    if result == "quit":
        break
    total = process_delivery(total, result)
    tax = calculate_tax(result)
    deliveries += 1

generate_report(total, deliveries, rejected)

