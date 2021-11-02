#include <cs50.h>
#include <stdio.h>
int main(void)
{
    // Prompt user. Hint: do while LOOPS and get_int
    int n;
    do
    {
        n = get_int("Height: ");
    }
    while (n < 1 || n > 8);

    // Jump to the other line
    for (int i = 1; i <= n; i++)
    {
        // Add the Spaces
        for (int s = n - 1; i <= s; s--)
        {
            printf(" ");
        }
        // Add the Hashes
        for (int j = 0; i > j; j++)
        {
            printf("#");
        }
        printf("\n");
    }
}