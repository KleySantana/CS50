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

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    // This one is tricky... You need to swap the contents of a pixel. The class swap.c can be usefull.
    // You'll need a temporary variable and use pointers to the original pixels.
    // The problem is: how to make it swap the pixels exactly to it's opposite?
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
    //This one is even more tricky. There's some crazy math to do to move the attention of the computer around each pixel.
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
            
            for (int a = -1; a < 2; a++)
            {
                for (int b = -1; b < 2; b++)
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

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    // This one is tricky++. 
    RGBTRIPLE temp[height][width];
    int GX[3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};
    int GY[3][3] = {{-1, -2, -1}, {0, 0, 0}, {1, 2, 1}};
    
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
            int rgx = 0;
            int ggx = 0;
            int bgx = 0;
            int rgy = 0;
            int ggy = 0;
            int bgy = 0;
            for (int a = 0; a < 3; a++)
            {
                for (int b = 0; b < 3; b++)
                {
                    // Condition to see if there's a major color diference between each pixel.
                    if (i - 1 + a < 0 || i - 1 + a > height - 1 || j - 1 + b < 0 || j - 1 + b > width - 1)
                    {
                        continue;
                    }
                    // Then, calculate the new edge color to highlight, and store the value at the temporary image 
                    rgx = rgx + (temp[i - 1 + a][j - 1 + b].rgbtRed * GX[a][b]);
                    ggx = ggx + (temp[i - 1 + a][j - 1 + b].rgbtGreen * GX[a][b]);
                    bgx = bgx + (temp[i - 1 + a][j - 1 + b].rgbtBlue * GX[a][b]);
                    
                    rgy = rgy + (temp[i - 1 + a][j - 1 + b].rgbtRed * GY[a][b]);
                    ggy = ggy + (temp[i - 1 + a][j - 1 + b].rgbtGreen * GY[a][b]);
                    bgy = bgy + (temp[i - 1 + a][j - 1 + b].rgbtBlue * GY[a][b]);
                }
            }
            // Calculate the square root
            float r = sqrt((rgx * rgx) + (rgy * rgy));
            float g = sqrt((ggx * ggx) + (ggy * ggy));
            float b = sqrt((bgx * bgx) + (bgy * bgy));
            // Round the square root
            int R = round(r);
            int G = round(g);
            int B = round(b);
            // Check if the value is higher than 255. If so, set it as 255.
            if (R > 255)
            {
                R = 255;
            }
            if (G > 255)
            {
                G = 255;
            }
            if (B > 255)
            {
                B = 255;
            }
            // Swap values from temp to original image
            image[i][j].rgbtRed = R;
            image[i][j].rgbtGreen = G;
            image[i][j].rgbtBlue = B;
        }
    }
    return;
}