from cs50 import get_int


def main():
    # Prompt user for height
    while True:
        height = get_int("Height: ")
        if height > 0 and height < 9:
            break
    # Call the function that prints the piramid
    hashes(height)
    
    
def hashes(height):
    i = 1
    # Add on line
    while i <= height:
        # At every end of the line it will return to the status quo and reassign the variables' values
        # The number of spaces should be the oposit of hashes
        s = height - i
        j = 0
        while s > 0:
            print(" ", end="")
            s -= 1
        while i > j:
            print("#", end="")
            j += 1
        print()
        i += 1
        
        
# Since I'm using custom functions, it's necessary to call main only at the end
main()