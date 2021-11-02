from cs50 import get_float


def main():
    # Prompt user
    while True:
        d = get_float("Change Owed: ")
        if d > 0:
            break
    helper(d)
    
    
def helper(d):
    # Change dollar to cents
    c = round(d * 100)
    # Count coins
    counter = 0
    while c > 24:
        c = c - 25
        counter += 1
    while c > 9:
        c = c - 10
        counter += 1
    while c > 4:
        c = c - 5
        counter += 1
    # This one will take what's left from int c, and add it to the counter since will always be 1-4.
    counter = counter + c
    print(f"{counter}")
    

main()