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

def generate_report(total_unit,failed_attemps):
    print(f'Total Deliveries Processed: {total_unit}')
    print(f'Number of Failed Entries: {failed_attemps}')

def load_inventory():
    try:
        with open('inventory.txt', 'r') as file:
            data = file.read()
            print(data)
    except FileNotFoundError:
        print('File not found, creating new Inventory file...')
        with open('inventoryy.txt', 'a') as file:
            data = file.write()

def save_inventory():
    x

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

generate_report(deliveries, rejected)

