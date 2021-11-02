#include <stdio.h>
#include <cs50.h>

int main(void)
{
    // Greetings
    string answer = get_string("What's your name? ");
    printf("Hello, %s\n.", answer);
}