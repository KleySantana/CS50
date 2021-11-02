def main():
    # Prompt user for input
    text = input("Text: ")
    # Counting
    l = count_letters(text)
    w = count_words(text) + 1
    s = count_sentences(text)
    # Coleman-Liau's formula
    index = round(0.0588 * (100 * l / w) - 0.296 * (100 * s / w) - 15.8)
    # Print Result
    if index < 1:
        print("Before Grade 1")
    elif index > 16:
        print("Grade 16+")
    else:
        print(f"Grade {index}")


# To count letter, isalpha will take care to see if all characters are letters. If not, will retur false.
def count_letters(text):
    count = 0
    for i in range(len(text)):
        if text[i].isalpha():
            count += 1
    return count
    
    
# Words are conted by the spaces + 1.
def count_words(text):
    count = 0
    for i in range(len(text)):
        if text[i].isspace():
            count += 1
    return count
    
    
# Sentences are every punctuation defined below
def count_sentences(text):
    count = 0
    for i in range(len(text)):
        if text[i] == "." or text[i] == "?" or text[i] == "!":
            count += 1
    return count
    

main()