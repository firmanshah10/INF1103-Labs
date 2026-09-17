total = 0
rejected = 0

while True:
    entry = input("Enter a stock quantity (or quit): ")
    if entry == "quit":
        break
    if entry.isdigit():
        integer_entry = int(entry)
        total+= integer_entry
        if total > 500:
            print("You have exceeded the maximum stock limit of 500")
            break
    else:
        print("Invalid input, please enter a whole number")
        rejected +=1
print("Total Stock Quantity:", total)
print("Rejected Entries", rejected)
