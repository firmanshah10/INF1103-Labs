total = 0
rejected = 0

while True:
    entry = input("Enter a stock quantity (or quit): ")
    if entry == "quit":
        break
    if entry.isdigit():
        int_entry = int(entry)
        total += int_entry
        if total > 500:
            print("You have exceeded the maximum stock limit of 500")
            break
    else:
        print("Invalid input. Ple49" \
        "Please enter a valid number or quit: ")
        rejected +=1
print("Total Stock Quantity: ", total)
print("Rejected Entries: ", rejected)



