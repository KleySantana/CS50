#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void)
{
    // How much do you owe
    float d;
    do
    {
        d = get_float("Change owed: ");
    }
    while (d < 0);

    // Change Dollar to cents
    int c = round(d * 100);

    // Counter
    int counter = 0;
    while (c > 24)
    {
        c = (c - 25);
        counter++;
    }
    while (c > 9)
    {
        c = (c - 10);
        counter++;
    }
    while (c > 4)
    {
        c = (c - 5);
        counter++;
    }
    // This one will take what's left from int c, and add it to the counter since will always be between1-4.
    counter = counter + c;
    printf("%i\n", counter);
}