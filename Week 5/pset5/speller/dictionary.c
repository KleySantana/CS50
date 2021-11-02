// Implements a dictionary's functionality
#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#include <stdlib.h>
#include <strings.h>
#include <ctype.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

int wordcount = 0;

// Number of buckets in hash table
const unsigned int N = 26 ^ 5;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    int len = strlen(word);
    char copy[len + 1];
    copy[len] = '\0';
    
    for (int i = 0; i < len; i++)
    {
        copy[i] = tolower(word[i]);
    }
    int hs = hash(copy);
    node *h = table[hs];
    if (h == NULL)
    {
        return false;
    }
    while (h != NULL)
    {
        if (strcasecmp(h->word, copy) == 0)
        {
            return true;
        }
        h = h->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // Hash function by delipity on reddit.
    unsigned int h = 0;
    for (int i = 0, n = strlen(word); i < n; i++)
    {
        h = (h << 2) ^ word[i];
    }
    return h % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // Open dictionary file
    const char *d = dictionary;
    FILE *file = fopen(d, "r");
    if (file == NULL)
    {
        return false;
    }

    // Read strings from file one at a time
    char word[LENGTH + 1];
    while (fscanf(file, "%s", word) != EOF)
    {
        node *n = malloc(sizeof(node));
        // Create a new node for each word
        if (n == NULL)
        {
            fclose(file);
            return false;
        }
        strcpy(n->word, word);
        n->next = NULL;
        
        // Hash word to obtain a hash value
        unsigned int x = hash(word);

        // Insert node into hash table at that location
        n->next = table[x];
        table[x] = n;
        
        wordcount++;
    }
    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return wordcount;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        node *n = table[i];
        node *cursor = n;

        while (cursor != NULL)
        {
            node *tmp = cursor;
            cursor = cursor->next;
            free(tmp);
        }
    }
    return true;
}