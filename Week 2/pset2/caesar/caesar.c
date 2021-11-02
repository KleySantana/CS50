#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <stdlib.h>


// Check the CS50 Manual Pages. The function `isdigit()` will check whether a character is a digit, not a whole string. So you need to loop over and iterate over the length of the `string argv[1`] to check if it's a digit. Only then you can `atoi argv[1]`.
//To sum up, you can't just write
//`if (argc == 2 && isdigit(argv[1])`
//Try doing something like this:
//```
//for (int i = 0; i < strlen(argv[1]); i++)
//        {
            //if ((isdigit(argv[i])) == 0)
          //  {
        //        printf("Usage: ...");
      //          return 1;
    //        }
  //      }
//```
int main(int argc, string argv[])
{
    // Make sure the comand-line argument is only one and it's a number
    string k = argv[1];
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    else
    {
        for (int i = 0; i < strlen(k); i++)
        {
            if ((isdigit(k[i])) == 0)
            {
                printf("Usage: ./caesar key\n");
                return 1;
            }
        }
    }

    // Change string number to an integer
    int key = atoi(k);

    // Ask user for imput
    string text = get_string("plaintext: ");

    // Convert plaitext to ciphertext
    for (int i = 0; i < strlen(text); i++)
    {
        if (isupper(text[i]))
        {
            // In ASCII capital A = 65. That formula changes each letter by the key and maintain it lower case or upper case.
            text[i] = (text[i] - 65);
            text[i] = (text[i] + key) % 26;
            text[i] = (text[i] + 65);
        }
        if (islower(text[i]))
        {
            text[i] = (text[i] - 97);
            text[i] = (text[i] + key) % 26;
            text[i] = (text[i] + 97);
        }
        // This one keeps the numbers and punctuations as it is
        if (isalpha(text[i] == 0))
        {
            text[i] = text[i];
        }
    }
    printf("ciphertext: %s\n", text);
}