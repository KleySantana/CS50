from cs50 import get_int
from math import floor

# Some variables
digit1 = 0
digit2 = 0
num_digits = 0
sum_of_double_odds = 0
sum_of_evens = 0
# Get input from user
cc_number = get_int("Number: ")

# Loop through every number
while cc_number > 0:
    digit2 = digit1
    digit1 = cc_number % 10

    if num_digits % 2 == 0:
        sum_of_evens += digit1
    else:
        multiple = 2 * digit1
        sum_of_double_odds += (multiple // 10) + (multiple % 10)
    # The //= is a floor division. It will truncate a division and remove the last digit from the variable.
    cc_number //= 10
    num_digits += 1

# Luhn's algorithm to validate the card
is_valid = (sum_of_evens + sum_of_double_odds) % 10 == 0
first_two_digits = (digit1 * 10) + digit2

if digit1 == 4 and num_digits >= 13 and num_digits <= 16 and is_valid:
    print("VISA")
elif first_two_digits >= 51 and first_two_digits <= 55 and num_digits == 16 and is_valid:
    print("MASTERCARD")
elif (first_two_digits == 34 or first_two_digits == 37) and num_digits == 15 and is_valid:
    print("AMEX")
else:
    print("INVALID")