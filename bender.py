import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.


class Map:

    def __init__(self, map_array, l, c):
        self.array = map_array
        self.l = l
        self.c = c
        height_map = len(map_array)
        width_map = len(map_array[0])
        print >> sys.stderr, 'Creating map with '+str(l)+' lines and '+str(c)+' columns, with height='+str(height_map) + 'and width='+str(width_map)
        assert len(map_array) == self.l
        assert len(map_array[0]) == self.c

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
        self.direction_index = -1
        self.direction_increment = 1
        self.current_dir = 'SOUTH'
        self.position = map.get_starting_point()
        self.done = False
        # For detecting loops, keep the cell and direction
        self.history = {}

    def next(self, mmap, (cell_x, cell_y)):
        ''' Change the state given the cell we go to '''
        cell_type = mmap.get(cell_x, cell_y)
        if cell_type == '#':
            # Try next direction
            
            self.direction_index = self.direction_index + self.direction_increment
            self.current_dir = self.directions[self.direction_index]
            print >> sys.stderr, 'Obstacle, trying to change direction to {}' .format(self.current_dir)

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
                self.direction_index = self.direction_index + self.direction_increment
                self.current_dir = self.directions[self.direction_index]
                print >> sys.stderr, 'Obstacle, trying to change direction to {}' .format(self.current_dir)

        elif cell_type == 'N':
            self.position = (cell_x, cell_y)
            # self.current_dir = 'NORTH'
            print >> sys.stderr, 'Modifier: going NORTH'
        elif cell_type == 'S':
            self.position = (cell_x, cell_y)
            #self.current_dir = 'SOUTH'
            print >> sys.stderr, 'Modifier: going SOUTH'
        elif cell_type == 'E':
            self.position = (cell_x, cell_y)
            # self.current_dir = 'EAST'
            print >> sys.stderr, 'Modifier: going EAST'
        elif cell_type == 'W':
            self.position = (cell_x, cell_y)
            # self.current_dir = 'WEST'
            print >> sys.stderr, 'Modifier: going WEST'

        else:
            raise Exception('Non handled cell type ' + str(cell_type))

        return self

    def reset_direction_state(self):
        print >> sys.stderr, 'Restarting direction switch state'
        self.direction_index = -1

    def add_history(self, x, y, direction):
        """ Returns True if added, False if a loop is detected """
        if (x,y) not in self.history:
            self.history[(x,y)] = []

        dirs = self.history.get((x,y))
        if direction in dirs:
            print >> sys.stderr, "LOOP DETECTED"
            return False
        else:
            self.history.get((x,y)).append(direction)
            return True
        

    def run(self, map):
        actions_array = []
        while not self.done:
            x, y = self.position


            # Check oif modify direction
            cell_type = map.get(x, y)
            if cell_type in ['N', 'S', 'E', 'W']:
                if cell_type == 'N':
                    self.current_dir = 'NORTH'
                elif cell_type == 'S':
                    self.current_dir = 'SOUTH'
                elif cell_type == 'W':
                    self.current_dir = 'WEST'
                elif cell_type == 'E':
                    self.current_dir = 'EAST'
                else:
                    raise Exception('Could not handle cell type at run stage: {}'.format(cell_type))


            if self.current_dir == 'SOUTH':
                next_pos = (x + 1, y)
            if self.current_dir == 'EAST':
                next_pos = (x, y + 1)
            if self.current_dir == 'NORTH':
                next_pos = (x - 1, y)
            if self.current_dir == 'WEST':
                next_pos = (x, y - 1)

            old_dir = self.current_dir

            print >> sys.stderr, 'Trying direction {}'.format(self.current_dir)
            self = self.next(map, next_pos)
            if self.position != (x, y):
                print >> sys.stderr, 'Moving to {}'.format(str(self.position))
                print old_dir
                no_loop = self.add_history(x, y, old_dir)
                if not no_loop:
                    print 'LOOP'
                    actions_array.append('LOOP')
                    return actions_array
                actions_array.append(old_dir)
                self.reset_direction_state()


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
    process(map_array, l, c)
    



if __name__ == '__main__':
    main()