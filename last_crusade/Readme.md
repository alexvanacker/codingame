## Game Input

The program must first read the initialization data from standard input. Then, within an infinite loop, read the data from the standard input related to the current position of Indy and provide to the standard output the expected data.
Initialization input
Line 1: 2 space separated integers W H specifying the width and height of the grid.

Next H lines: each line represents a line in the grid and contains W space separated integers T. T specifies the type of the room.

Last line: 1 integer EX specifying the coordinate along the X axis of the exit (this data is not useful for this first mission, it will be useful for the second level of this puzzle).

## Input for one game turn

Line 1: XI YI POS
(XI, YI) two integers to indicate Indy's current position on the grid.
POS a single word indicating Indy's entrance point into the current room: TOP if Indy enters from above, LEFT if Indy enters from the left and RIGHT if Indy enters from the right.

## Output for one game turn

A single line with 2 integers: X Y representing the (X, Y) coordinates of the room in which you believe Indy will be on the next turn.

## Constraints
0 < W ≤ 20
0 < H ≤ 20
0 ≤ T ≤ 13
0 ≤ EX < W
0 ≤ XI, X < W
0 ≤ YI, Y < H

Response time for one game ≤ 150ms