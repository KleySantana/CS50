#include "helpers.h"
#include <math.h>

// Convert image to grayscale
// Em cada pixel tire a média dos valores RGB e atribua o valor médio a cada valor de RGB
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    //Pense na imagem como um array bi-dimensional. O código deve entrar em image[0][0] e tirar a média da estrutura RGBTRIPLE.
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float average = (((float)image[i][j].rgbtRed + (float)image[i][j].rgbtGreen + (float)image[i][j].rgbtBlue) / 3);
            image[i][j].rgbtRed = round(average);
            image[i][j].rgbtGreen = round(average);
            image[i][j].rgbtBlue = round(average);
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    int k;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int sepiaRed = round((0.393 * image[i][j].rgbtRed) + (0.769 * image[i][j].rgbtGreen) + (0.189 * image[i][j].rgbtBlue));
            int sepiaGreen = round((0.349 * image[i][j].rgbtRed) + (0.686 * image[i][j].rgbtGreen) + (0.168 * image[i][j].rgbtBlue));
            int sepiaBlue = round((0.272 * image[i][j].rgbtRed) + (0.534 * image[i][j].rgbtGreen) + (0.131 * image[i][j].rgbtBlue));
            int SEPIA[] = {sepiaRed, sepiaGreen, sepiaBlue};
            for (k = 0; k < 3; k++)
            {
                if (SEPIA[k] < 0)
                {
                    SEPIA[k] = 0;
                }
                else if (SEPIA[k] > 255)
                {
                    SEPIA[k] = 255;
                }
            }
            image[i][j].rgbtRed = SEPIA[0];
            image[i][j].rgbtGreen = SEPIA[1];
            image[i][j].rgbtBlue = SEPIA[2];
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    // This one is tricky... You need to swap the contents of a pixel. The class swap.c can be usefull.
    // You'll need a temporary variable and use pointers to the original pixels.
    // The problem is: how to make it swap the pixels exactly to it's opposite?
    
    //Temporary variable
    RGBTRIPLE imtmp[width];
    
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            imtmp[(width - 1) - j] = image[i][j];
        }
        for (int a = 0; a < width; a++)
        {
            image[i][a] = imtmp[a];
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // This one will average all pixels siding with image[i][j]
    RGBTRIPLE temp[height][width];

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            temp[i][j] = image[i][j];
        }
    }
    
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float count = 0.00;
            int sumR = 0;
            int sumG = 0;
            int sumB = 0;
            
            for (int a = - 1; a < 2; a++)
            {
                for (int b = - 1; b < 2; b++)
                {
                    if (i + a >= 0 && i + a < height && j + b >= 0 && j + b < width)
                    {
                        sumR += temp[i + a][j + b].rgbtRed;
                        sumG += temp[i + a][j + b].rgbtGreen;
                        sumB += temp[i + a][j + b].rgbtBlue;
                        count++;
                    }
                }
            }
            image[i][j].rgbtRed = round(sumR / count);
            image[i][j].rgbtGreen = round(sumG / count);
            image[i][j].rgbtBlue = round(sumB / count);
        }
    }
    return;
}