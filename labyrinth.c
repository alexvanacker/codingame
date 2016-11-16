#include <stdlib.h>
#include <stdio.h>
#include <string.h>



int main()
{
    int R; // number of rows.
    int C; // number of columns.
    int A; // number of rounds between the time the alarm countdown is activated and the time the alarm goes off.
    scanf("%d%d%d", &R, &C, &A);

    // game loop
    while (1) {
        int KR; // row where Kirk is located.
        int KC; // column where Kirk is located.
        scanf("%d%d", &KR, &KC);
        for (int i = 0; i < R; i++) {
            char ROW[C+1]; // C of the characters in '#.TC?' (i.e. one line of the ASCII maze).
            scanf("%s", ROW);
        }

        // Write an action using printf(). DON'T FORGET THE TRAILING \n
        // To debug: fprintf(stderr, "Debug messages...\n");

        printf("RIGHT\n"); // Kirk's next move (UP DOWN LEFT or RIGHT).
    }

    return 0;
}