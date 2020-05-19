#include <stdio.h>
#include <memory.h>
#include <stdlib.h>
#include <errno.h>

#define OPEN_FILE_ERR "Error opening file:"
#define HEADER ">"
#define BASE 10
#define ARG_NUM_ERR "Error: wrong number of argunets, should be 5 arguments."
#define SEQ_NUM_ERR "Error: wrong number of sequences, should be at least 2 sequences"
#define INVALID_ARG "Error: invalid argument, should be an integer"


int readFile(FILE* p, char** ptrArr, char** headerArr)
{
    char lineBuff[100];
    size_t seqSize = 0;
    int seqCount = 0;
    fgets(lineBuff, 100, p);
    while (!feof(p))
    {
        int result = strncmp(HEADER, lineBuff, 1);
        if (!result)
        {
            lineBuff[strcspn(lineBuff, "\r")] = '\0';
            lineBuff[strcspn(lineBuff, "\n")] = '\0';
            size_t buffLen = strlen(lineBuff);
            headerArr[seqCount] = (char *) calloc(buffLen, buffLen);
            char* seqName = (char *) calloc(buffLen, buffLen);
            memmove(seqName, lineBuff, buffLen);
            strcat(headerArr[seqCount], seqName + 1);
            fgets(lineBuff, 100, p);
            lineBuff[strcspn(lineBuff, "\r")] = '\0';
            lineBuff[strcspn(lineBuff, "\n")] = '\0';
            ptrArr[seqCount] = (char*) calloc(seqSize, seqSize);
            while (strncmp(HEADER, lineBuff, 1) != 0 && !feof(p))
            {
                seqSize += strlen(lineBuff);
                ptrArr[seqCount] = (char*) realloc(ptrArr[seqCount], seqSize + 1);
                strcat(ptrArr[seqCount], lineBuff);
                fgets(lineBuff, 100, p);
                lineBuff[strcspn(lineBuff, "\r")] = '\0';
                lineBuff[strcspn(lineBuff, "\n")] = '\0';
            }
            free(seqName);
        }
        seqCount += 1;
        seqSize = 0;
    }
    if (seqCount < 2)
    {
        fprintf(stderr, "%s\n", SEQ_NUM_ERR);
        exit(EXIT_FAILURE);
    }
    return seqCount;
}

int** initTable(char* x, char* y, int g)
{
    size_t m = strlen(x);
    size_t n = strlen(y);
    int** table = (int**) malloc((m + 1) * sizeof(int*));
    for (int i = 0; i < m + 1; i++)
    {
        table[i] = (int*) malloc((n + 1) * sizeof(int));
    }
    table[0][0] = 0;
    for (int i = 1; i < m + 1; i++)
    {
        table[i][0] = g * i;
    }
    for (int j = 1; j < n + 1; j++)
    {
        table[0][j] = g * j;
    }
    return table;
}

int firstMatch(int** f, char* x, char* y, int ind1, int ind2, int match, int missMatch)
{
    int currentVal = 0;
    int result = strncmp(&x[ind1 - 1], &y[ind2 - 1], 1);
    if(!result)
    {
        currentVal = f[ind1 - 1][ind2 -1] + match;
    }
    else {
        currentVal = f[ind1 - 1][ind2 -1] + missMatch;
    }
    return currentVal;
}

int secondMatch(int** f, int ind1, int ind2, int gap)
{
    int currentVal = 0;
    int firstVal = f[ind1][ind2 - 1] + gap;
    int secondVal = f[ind1 - 1][ind2] + gap;
    if (firstVal > secondVal)
    {
        currentVal = firstVal;
    }
    else
    {
        currentVal = secondVal;
    }
    return currentVal;
}

int findMatch(char* x, char* y, int match, int missMatch, int gap)
{
    int score = 0;
    int tempVal1;
    int tempVal2;
    size_t m = strlen(x);
    size_t n = strlen(y);
    int** table = initTable(x, y, gap);
    for (int i = 1; i < m + 1; i++)
    {
        for (int j = 1; j < n + 1; j++)
        {
            tempVal1 = firstMatch(table, x, y, i, j, match, missMatch);
            tempVal2 = secondMatch(table, i, j, gap);
            if (tempVal1 > tempVal2){
                score = tempVal1;
            }
            else
            {
                score = tempVal2;
            }
            table[i][j] = score;
        }
    }
    int finalScore = table[m][n];
    for (int k = 0; k < m; k++)
    {
        free(table[k]);
    }
    return finalScore;
}

void combine(char** ptrArr, char** headerArr, int match, int missMatch, int gap, int seqNum)
{
    for (int i = 0; i < seqNum; i++)
    {
        for (int j = i + 1; j < seqNum; j++)
        {
            int val = findMatch(ptrArr[i], ptrArr[j], match, missMatch, gap);
            printf("Score for alignment of %s to %s is %d\n", headerArr[i], headerArr[j], val);
        }
    }
}

int convertArg(char* num)
{
    char* ptr;
    int result;
    errno = 0;
    result = (int) strtol(num, &ptr, BASE);
    if (!result && (errno || ptr == num)){
        fprintf(stderr, INVALID_ARG);
        exit(EXIT_FAILURE);
    }
    return result;
}

int main(int agrc, char *argv[])
{
    if (agrc != 5)
    {
        fprintf(stderr, "%s\n", ARG_NUM_ERR);
        exit(EXIT_FAILURE);
    }
    int m = convertArg(argv[2]);
    int s = convertArg(argv[3]);
    int g = convertArg(argv[4]);
    FILE *fp = fopen(argv[1], "r");
    if (!fp)
    {
        fprintf(stderr, "%s %s\n", OPEN_FILE_ERR, argv[1]);
        exit(EXIT_FAILURE);
    }
    char *ptrArray[100];
    char *headerArray[100];
    int numOfSeq = readFile(fp, ptrArray, headerArray);
    combine(ptrArray, headerArray, m, s, g, numOfSeq);
    for (int num = 0; num < numOfSeq; num++)
    {
        free(ptrArray[num]);
        free(headerArray[num]);
    }
    return 0;
}

