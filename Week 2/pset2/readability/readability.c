#include <cs50.h>
#include <stdio.h>
#include <math.h>
#include <ctype.h>
#include <string.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    // Prompt the user for input
    string text = get_string("Text: ");
    // Counting
    float l = (int)count_letters(text);
    float w = (int)count_words(text) + 1;
    float s = (int)count_sentences(text);
    // Coleman-Liau formula
    float index = round(0.0588 * (100 * l /  w) - 0.296 * (100 * s / w) - 15.8);
    // Print result
    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index > 16)
    {
        printf("Grade 16+\n");
    }
    else if (index >= 1 || index <= 16)
    {
        printf("Grade %i\n", (int)index);
    }
}

int count_letters(string text)
{
    int count = 0;

    for (int i = 0, len = strlen(text); i < len; i++)
    {
        if (isalpha(text[i]))
        {
            count++;
        }
    }
    return count;
}
// Counting letters: Done

// Next: count words
int count_words(string text)
{
    int countw = 0;

    for (int i = 0, len = strlen(text); i < len; i++)
    {
        if (isblank(text[i]))
        {
            countw++;
        }
    }
    return countw;
}
// Counting words: done

// Next: Count sentences
int count_sentences(string text)
{
    int counts = 0;

    for (int i = 0, len = strlen(text); i < len; i++)
    {
        if ((text[i] == '.') || (text[i] == '?') || (text[i] == '!'))
        {
            counts++;
        }
    }
    return counts;
}
//Counting sentences: Done