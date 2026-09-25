total = 0
def get_valid_input():
    while True:
        entry = input("Enter a stock quantity (or quit): ")
        if entry == "quit":
            return "quit"
        if entry.isdigit():
            return int(entry)
        else:
            print("Invalid input, please enter a valid input")

def process_delivery(total, result):
    new_total = total + result
    return new_total
    