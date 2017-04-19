import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

class Map:

    def __init__(self, map_array, l, c):
        self.array = map_array
        self.l = l
        self.c = c

    def get(self, x, y):
        return self.array[x][y]

    def get_starting_point(self):
        for x in range(0, self.l):
            for y in range(0, self.c):
                if self.array[x][y] == '@':
                    return (x, y)



class BenderState:


    def __init__(self, map):
        self.inversion_activated = False
        self.breaker_mode = False
        self.directions = ['S', 'E', 'N', 'W']
        self.current_dir = 'S'
        self.position = map.get_starting_point()

    def next_step(self, map):
        x, y = self.position
        next_pos_type = None
        if self.current_dir == 'S':
            next_pos_type = map.get(x-1, y)
        if self.current_dir == 'E':
            next_pos_type = map.get(x, y+1)
        if self.current_dir == 'N':
            next_pos_type = map.get(x+1, y)
        if self.current_dir == 'W':
            next_pos_type = map.get(x, y-1)

        if next_pos_type == '#':
            self.current_dir = directions[]
        

   

def process(map_array):
    map = Map(map_array)






def main():
    l, c = [int(i) for i in raw_input().split()]
    print >> sys.stderr, "l=" + str(l) + ", c="+str(c)
    map_array = []
    for i in xrange(l):
        row = raw_input()
        print >> sys.stderr, row
        map_array.append(row)
    print "answer"


if __name__ == '__main__':
    main()