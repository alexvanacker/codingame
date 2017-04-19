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

    def remove_obstacle(self, x, y):
        self.array[x][y] = ' '


class BenderState:

    def __init__(self, map):
        # Should be the same as direction_increment
        self.inversion_activated = False
        self.breaker_mode = False
        self.directions = ['SOUTH', 'EAST', 'NORTH', 'WEST']
        self.direction_increment = 1
        self.current_dir = 'SOUTH'
        self.position = map.get_starting_point()
        self.done = False

    def next(self, mmap, (cell_x, cell_y)):
        ''' Change the state given the cell we go to '''
        cell_type = mmap.get(cell_x, cell_y)
        if cell_type == '#':
            # Increment the direction
            dir_index = self.directions.index(self.current_dir) + self.direction_increment
            self.current_dir = self.directions[dir_index]

        elif cell_type == ' ':
            #  Move in the current direction
            self.position = (cell_x, cell_y)

        elif cell_type == '$':
            self.position = (cell_x, cell_y)
            self.done = True

        elif cell_type == 'I':
            # move to the cell
            self.position = (cell_x, cell_y)
            # Change the direction increment
            self.direction_increment = -self.direction_increment

        elif cell_type == 'B':
            self.position = (cell_x, cell_y)
            self.breaker_mode = not self.breaker_mode
        elif cell_type == 'X':
            if self.breaker_mode:
                # Break
                self.position = (cell_x, cell_y)
                # Remove X from map
                mmap.remove_obstacle(cell_x, cell_y)
                pass
            else:
                dir_index = self.directions.index(self.current_dir) + self.direction_increment
                self.current_dir = self.directions[dir_index]

        elif cell_type == 'N':
            self.position = (cell_x, cell_y)
            self.current_dir = 'NORTH'
        elif cell_type == 'S':
            self.position = (cell_x, cell_y)
            self.current_dir = 'SOUTH'
        elif cell_type == 'E':
            self.position = (cell_x, cell_y)
            self.current_dir = 'EAST'
        elif cell_type == 'W':
            self.position = (cell_x, cell_y)
            self.current_dir = 'WEST'

        else:
            raise Exception('Non handled cell type ' + str(cell_type))

        return self

    def run(self, map):
        actions_array = []
        while not self.done:
            x, y = self.position
            if self.current_dir == 'SOUTH':
                next_pos = (x + 1, y)
            if self.current_dir == 'EAST':
                next_pos = (x, y + 1)
            if self.current_dir == 'NORTH':
                next_pos = (x - 1, y)
            if self.current_dir == 'WEST':
                next_pos = (x, y - 1)

            self = self.next(map, next_pos)
            if self.position != (x, y):
                print >> sys.stderr, 'Moving to {}'.format(str(self.position))
                print self.current_dir
                actions_array.append(self.current_dir)
        return actions_array


def process(map_array, lines, columns):
    mmap = Map(map_array, lines, columns)
    state = BenderState(mmap)
    actions = state.run(mmap)
    return actions

def main():
    l, c = [int(i) for i in raw_input().split()]
    print >> sys.stderr, "l=" + str(l) + ", c="+str(c)
    map_array = []
    for i in xrange(l):
        row = raw_input()
        print >> sys.stderr, row
        map_array.append(row)
    



if __name__ == '__main__':
    main()