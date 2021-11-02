#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, string argv[])
{
    // Make sure argument count is 2.
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }
    string k = argv[1];
    // Make sure it's only alphabet-based
    for (int i = 0, len = strlen(k); i < len; i++)
    {
        if ((isalpha(k[i])) == 0)
        {
            printf("Usage: ./substitution key\n");
            return 1;
        }
        // Make sure it has 26 letters
        if (len != 26)
        {
            printf("Key must contain 26 characters\n");
            return 1;
        }
        // Make sure it doesn't have repeated characters
        char i_C = k[i];
        for (int j = 0, len1 = strlen(k); j < len1; j++)
        {
            char j_C = k[j];
            if (toupper(i_C) == toupper(j_C) && i != j)
            {
                printf("Key must not contain repeated characters.\n");
                return 1;
            }
        }
    }
    // Argument validation ok.
    // Now encipher.

    string text = get_string("plaintext: ");

    //  Go through the text and substitute each letter with the key
    char c;
    int l = strlen(text);
    char ciphertext[l];
    int value;

    for (int i = 0; i <= l; i++)
    {
        if (isalpha(text[i]) && isupper(text[i]))
        {
            value = text[i] - 65;
            c = (toupper(k[value]));
        }
        else if (isalpha(text[i]) && islower(text[i]))
        {
            value = text[i] - 97;
            c = (tolower(k[value]));
        }
        else
        {
            c = text[i];
        }
        ciphertext[i] = c;
    }
    printf("ciphertext: %s\n", ciphertext);
}