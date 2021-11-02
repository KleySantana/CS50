import csv
import sys
import re


# Check for 3 arguments
if len(sys.argv) != 3:
    sys.exit("Usage: python dna.py database/F.csv sequences/0.txt")

# Open the csv file and dna sequence, then read them into memory.
nucleotides = []
with open(sys.argv[1], "r") as database:
    person_of_interest = list(csv.reader(database))
    nucleotides = person_of_interest[0]

# Open txt file
with open(sys.argv[2], "r") as dna:
    sequence = dna.read()

# For each str, compute the longest run of consecutive repeats in the dna sequence

STRs = []
for i in range(1, len(nucleotides)):
    x = re.findall(rf'(?:{nucleotides[i]})+', sequence)
    if len(x) == 0:
        STRs.append(0)
    else:
        STRs.append(len(max(x, key=len)) // len(nucleotides[i]))

# Turn STRs into a list of strings
STRs = list(map(str, STRs))
person = list(person_of_interest)
person.pop(0)
# Compare the STRs against each row in the csv file
for i in person:
    if i[1:] == STRs:
        print(f"{i[0]}")
        break
    elif i == person_of_interest[-1]:
        print("No match")