#include <cs50.h>
#include <stdio.h>

int main(void)

{
    // Prompt for start size
    int n;
    do
    {
        n = get_int("Current population: ");
    }
    while (n < 9);

    // Prompt for end size
    int s;
    do
    {
        s = get_int("Final Population: ");
    }
    while (s < n);

    // Keep Track number of years
    int y = 0;

    // Calculate number of years until we reach threshold
    while (n < s)
    {
        n = n + (n / 3) - (n / 4);
        y++;
    }
    // Print number of years
    {
        printf("Years: %i\n", y);
    }
}