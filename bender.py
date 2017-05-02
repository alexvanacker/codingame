import sys

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.


class Map:

    def __init__(self, map_array, l, c):
        self.array = map_array
        self.l = l
        self.c = c
        height_map = len(map_array)
        width_map = len(map_array[0])
        print >> sys.stderr, 'Creating map with ' + str(l) + ' lines and ' + str(c) + ' columns, with height=' + str(height_map) + 'and width=' + str(width_map)
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

        new_map_array = []
        for i, column in enumerate(self.array):
            if i != x:
                new_map_array.append(self.array[i])
            else:
                new_column = []
                for j, cell in enumerate(self.array[i]):
                    if j == y:
                        print >> sys.stderr, 'Removing obstacle at {} {}'.format(x, y)
                        new_column.append(' ')
                    else:
                        new_column.append(cell)

                new_map_array.append(new_column)
        self.array = new_map_array

    def get_other_teleport(self, x, y):
        for i in range(0, self.l):
            for j in range(0, self.c):
                if self.array[i][j] == 'T':
                    if i != x or j != y:
                        return (i, j)
        raise Exception('Could not find other teleport')

    def get_cell_with_direction(self, x, y, direction):
        """ Return the cell and cell type as a tuple (x, y, cell_type)
        you would reach by going from (x, y) in the given direction.
        Note: x is from down to up, and y from left to right
        """

        (x_increment, y_increment) = get_position_increments_for_direction(direction)
        new_x = x + x_increment
        new_y = y + y_increment
        # print >> sys.stderr, 'Getting cell at {}'.format((str(new_x), str(new_y)))
        new_cell_type = self.get(new_x, new_y)

        return (new_x, new_y, new_cell_type)


class BenderState:

    def __init__(self, map):
        # Should be the same as direction_increment
        self.breaker_mode = False
        self.directions = ['SOUTH', 'EAST', 'NORTH', 'WEST']
        self.direction_index = -1
        self.direction_increment = 1
        self.current_dir = 'SOUTH'
        self.position = map.get_starting_point()
        self.done = False
        self.history = []
        self.direction_history = []

    def next2(self, mmap):
        """ A more 'FSM' implementation """
        # Get the next cell according to the direction
        (next_x, next_y, cell_type) = mmap.get_cell_with_direction(self.position[0], self.position[1], self.current_dir)
        if cell_type == ' ':
            self.move()
        elif cell_type == 'B':
            self.move()
            self.change_breaker_mode()
        elif cell_type == '$':
            self.move()
            self.finish()
        elif cell_type == 'X':
            if self.breaker_mode:
                mmap.remove_obstacle(next_x, next_y)
                self.move()
            else:
                self.change_direction()
        elif cell_type == '#':
            self.change_direction()
        elif cell_type == 'I':
            self.invert_directions()
            self.move()
        elif cell_type == 'T':
            self.move()
            self.teleport(next_x, next_y, mmap)
        elif cell_type in ['N', 'S', 'W', 'E']:
            self.move()
            self.set_direction(cell_type)
        else:
            raise Exception('Unhandled cell type {} at {}'.format(cell_type, (next_x, next_y)))

    def teleport(self, x, y, mmap):
        (other_x, other_y) = mmap.get_other_teleport(x, y)
        self.position = (other_x, other_y)
        print >> sys.stderr, 'Going to teleport at {}'.format(str(self.position))

    def set_direction(self, direction_letter):
        """ Change direction because of direction modifier. """
        if direction_letter == 'N':
            self.current_dir = 'NORTH'
        elif direction_letter == 'S':
            self.current_dir = 'SOUTH'
        elif direction_letter == 'W':
            self.current_dir = 'WEST'
        elif direction_letter == 'E':
            self.current_dir = 'EAST'
        print >> sys.stderr, 'Changing direction to {}'.format(self.current_dir)

    def invert_directions(self):
        self.directions.reverse()
        print >> sys.stderr, 'Inverter mode: reversing directions to {}'.format(self.directions)

    def change_breaker_mode(self):
        self.breaker_mode = not self.breaker_mode
        print >> sys.stderr, 'Changing breaker mode to {}'.format(str(self.breaker_mode))

    def move(self):
        """ Move in the current direction """
        x_increment, y_increment = get_position_increments_for_direction(self.current_dir)
        x, y = self.position
        self.position = (x + x_increment, y + y_increment)
        self.direction_history.append(self.current_dir)
        print >> sys.stderr, 'Moved to {}, direction {}'.format(self.position, self.current_dir)
        self.reset_direction_state()

    def change_direction(self):
        """ Change direction """
        self.direction_index = self.direction_index + self.direction_increment
        self.current_dir = self.directions[self.direction_index]
        print >> sys.stderr, 'Changing direction to {}' .format(self.current_dir)

    def finish(self):
        print >> sys.stderr, 'Reached exit $'
        self.done = True

    def reset_direction_state(self):
        self.direction_index = -1

    def run2(self, mmap):
        while not self.done:
            self.next2(mmap)

        return self.direction_history


def get_position_increments_for_direction(direction):
    """ Return the coordinate increment according to the direction. """
    x_increment = 0
    y_increment = 0
    if direction == 'SOUTH':
        x_increment = 1
        y_increment = 0
    elif direction == 'NORTH':
        x_increment = -1
        y_increment = 0
    elif direction == 'EAST':
        x_increment = 0
        y_increment = 1
    elif direction == 'WEST':
        x_increment = 0
        y_increment = -1
    else:
        raise Exception('Unhandled direction : '.format(direction))
    return (x_increment, y_increment)


def process(map_array, lines, columns):
    mmap = Map(map_array, lines, columns)
    state = BenderState(mmap)
    actions = state.run2(mmap)
    return actions


def main():
    l, c = [int(i) for i in raw_input().split()]
    print >> sys.stderr, "l=" + str(l) + ", c=" + str(c)
    map_array = []
    for i in xrange(l):
        row = raw_input()
        print >> sys.stderr, row
        map_array.append(row)
    actions = process(map_array, l, c)
    if 'LOOP' in actions:
        print 'LOOP'
    else:
        for a in actions:
            print a


if __name__ == '__main__':
    main()
