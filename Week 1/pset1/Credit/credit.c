#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void)
{
    // Prompt user for credit card number
    long long c = 0;
    do
    {
        c = get_long_long("Cardnumber: ");
    }
    while (c < 0);
    
    // Count digits of the card.
    int x = 0;
    long long d = c;
    while (d > 0)
    {
        d = d / 10;
        x++;
    }
    // The counting can't be diferent "!=" from 13, 15, 16
    if ((x != 13) && (x != 15) && (x != 16))
    {
        printf("INVALID\n");
    }
    
    // Luhn’s Algorithm to validate credit cards
    int n[x];
    
    for (int i = 0; i < x; i++)
    {
        n[i] = c % 10;
        c = c / 10;
    }
    
    int on[x];
    for (int i = 1; i < x; i++)
    {
        on[i] = n[i];
    }
    
    for (int i = 1; i < x; i += 2)
    {
        n[i] = n[i] * 2;
    }
    
    // Apply the algorithm on the credit cards
    int v = 0;
    int temp;
    
    // This code is for Visa
    if (x == 13)
    {
        for (int i = 0; i < x; i++)
        {
            temp = (n[i] % 10) + (n[i] / 10 % 10);
            v = v + temp;
        }
        if (on[12] == 4 && v % 10 == 0)
        {
            printf("VISA\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    // For American Express
    if (x == 15)
    {
        for (int i = 0; i < x; i++)
        {
            temp = (n[i] % 10) + (n[i] / 10 % 10);
            v = v + temp;
        }
        if (on[14] == 3 && v % 10 == 0 && (on[13] == 4 || on[13] == 7))
        {
            printf("AMEX\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    // For Visa and Mastercard. Visa uses both 13 and 16 digit card
    if (x == 16)
    {
        for (int i = 0; i < x; i++)
        {
            temp = (n[i] % 10) + (n[i] / 10 % 10);
            v = v + temp;
        }
        if (on[15] == 4 && v % 10 == 0)
        {
            printf("VISA\n");
        }
        // I tried to shorten a litle bit this next line,
        // but doing this (on[14] == (1 || 2 || 3 || 4 || 5)) won't work
        else if (on[15] == 5 && v % 10 == 0 && (on[14] == 1 || on[14] == 2 || on[14] == 3 || on[14] == 4 || on[14] == 5))
        {
            printf("MASTERCARD\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    // After finished it doesn't look so hard
    
}