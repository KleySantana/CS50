#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    //Check if there's 2 arguments
    if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }
    // Open file and check if argv[1] is a valid file format
    FILE *file = fopen(argv[1], "r");
    if (!file)
    {
        printf("Could not open file.\n");
        return 1;
    }
    
    FILE *image = NULL;
    // Create the 512b blocks
    BYTE bytes[512];
    int filecount = 0;
    // Variable of the output's name
    char Recovered[8];
    while (fread(bytes, sizeof(BYTE), 512, file) == 512)
    {
        if (bytes[0] == 0xff && bytes[1] == 0xd8 && bytes[2] == 0xff && (bytes[3] & 0xf0) == 0xe0)
        {
            // Recover or skip the first image
            if (filecount == 0)
            {
                // sprintf will put the second argument in the first argument's array and print only the array.
                // "%03i" will hold the spot for 3 interger at the variable "filecount".
                sprintf(Recovered, "%03i.jpg", filecount);
                image = fopen(Recovered, "w");
                fwrite(&bytes, sizeof(BYTE), 512, image);
                filecount++;
            }
            // Continue with other images
            else if (filecount > 0)
            {
                fclose(image);
                sprintf(Recovered, "%03i.jpg", filecount);
                image = fopen(Recovered, "w");
                fwrite(&bytes, sizeof(BYTE), 512, image);
                filecount++;
            }
        }
        else if (filecount > 0)
        {
            fwrite(&bytes, sizeof(BYTE), 512, image);
        }
    }
    fclose(file);
    fclose(image);
}