total = 0
rejected = 0

while True:
    entry = input("Enter a stock quantity (or quit): ")
    if entry == "quit":
        break
    if entry.isdigit():
        int_entry = int(entry)
        total += int_entry
        


