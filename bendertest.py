import unittest
import bender


class Test(unittest.TestCase):

    def testMapInit(self):
        map_array = ['#####',
                     '#@  #',
                     '#   #',
                     '#   #',
                     '#####']
        lines = 5
        columns = 5
        map = bender.Map(map_array, lines, columns)
        self.assertEquals('@', map.get(1, 1))
        self.assertEquals((1, 1), map.get_starting_point())

    def testMapGetCellWithDirection(self):
        map_array = ['#####',
                     '#@B #',
                     '#X  #',
                     '#   #',
                     '#####']
        lines = 5
        columns = 5
        map = bender.Map(map_array, lines, columns)
        (x, y, cell_type) = map.get_cell_with_direction(1, 1, 'EAST')
        self.assertEquals((1, 2, 'B'), (x, y, cell_type))
        (x, y, cell_type) = map.get_cell_with_direction(1, 1, 'SOUTH')
        self.assertEquals((2, 1, 'X'), (x, y, cell_type))

    def testSimpleSouth(self):
        map_array = ['#####',
                     '#@  #',
                     '#   #',
                     '#$  #',
                     '#####']
        lines = 5
        columns = 5
        actions = bender.process(map_array, lines, columns)
        self.assertEquals(['SOUTH', 'SOUTH'], actions)

    def testLoopDetect(self):
        map_array = ['#####',
                     '#$  #',
                     '#   #',
                     '#@  #',
                     '#####']
        lines = 5
        columns = 5
        actions = bender.process(map_array, lines, columns)
        self.assertEquals(['LOOP'], actions)

    def testInverter(self):
        map_array = ['##########',
                     '#    I   #',
                     '#        #',
                     '#       $#',
                     '#       @#',
                     '#        #',
                     '#       I#',
                     '#        #',
                     '#        #',
                     '##########']
        lines = 10
        columns = 10
        actions = bender.process(map_array, lines, columns)
        self.assertEquals(['SOUTH', 'SOUTH', 'SOUTH', 'SOUTH', 'WEST',
                           'WEST', 'WEST', 'WEST', 'WEST',
                           'WEST', 'WEST', 'NORTH',
                           'NORTH', 'NORTH', 'NORTH', 'NORTH', 'NORTH',
                           'NORTH',
                           'EAST', 'EAST', 'EAST', 'EAST', 'EAST',
                           'EAST', 'EAST', 'SOUTH', 'SOUTH'], actions)

    def testExample(self):
        map_array = ['######',
                     '#@E $#',
                     '# N  #',
                     '#X   #',
                     '######']
        lines = 5
        columns = 6
        actions = bender.process(map_array, lines, columns)
        self.assertEquals(['SOUTH', 'EAST',
                           'NORTH', 'EAST',
                           'EAST'], actions)

    def testCase2(self):
        map_array = ['########',
                     '# @    #',
                     '#     X#',
                     '# XXX  #',
                     '#   XX #',
                     '#   XX #',
                     '#     $#',
                     '########']
        lines = 8
        columns = 8
        actions = bender.process(map_array, lines, columns)
        self.assertEquals(['SOUTH', 'EAST',
                           'EAST', 'EAST', 'SOUTH',
                           'EAST', 'SOUTH',
                           'SOUTH', 'SOUTH'], actions)

    def testObstacleEastToSouth(self):
        map_array = ['####',
                     '#@ X',
                     '##$#']
        lines = 3
        columns = 4
        actions = bender.process(map_array, lines, columns)
        self.assertEquals(['EAST', 'SOUTH'], actions)

    def testpathModifier(self):
        map_array = ['##########',
                     '#        #',
                     '#  S   W #',
                     '#        #',
                     '#  $     #',
                     '#        #',
                     '#@       #',
                     '#        #',
                     '#E     N #',
                     '##########']
        lines = 10
        columns = 10
        actions = bender.process(map_array, lines, columns)
        expected = ['SOUTH', 'SOUTH', 'EAST', 'EAST', 'EAST', 'EAST', 'EAST',
                    'EAST',
                    'NORTH', 'NORTH', 'NORTH', 'NORTH', 'NORTH', 'NORTH',
                    'WEST', 'WEST', 'WEST', 'WEST', 'SOUTH', 'SOUTH']
        self.assertEquals(expected, actions)

    def testBreaker(self):
        map_array = ['#######',
                     '#@    #',
                     '#B    #',
                     '#X    #',
                     '#$    #'
                     '#######']
        lines = 5
        columns = 7
        actions = bender.process(map_array, lines, columns)
        expected = ['SOUTH', 'SOUTH', 'SOUTH']
        self.assertEquals(expected, actions)

    def testBreakerLoop(self):
        map_array = ['##########',
                     '#        #',
                     '#  @     #',
                     '#  B     #',
                     '#  S   W #',
                     '# XXX    #',
                     '#  B   N #',
                     '# XXXXXXX#',
                     '#       $#',
                     '##########']

        lines = 10
        columns = 10
        actions = bender.process(map_array, lines, columns)
        expected = ['SOUTH', 'SOUTH', 'SOUTH', 'SOUTH',
                    'EAST', 'EAST', 'EAST', 'EAST',
                    'NORTH', 'NORTH', 'WEST', 'WEST',
                    'WEST', 'WEST', 'SOUTH', 'SOUTH',
                    'SOUTH', 'SOUTH',
                    'EAST', 'EAST', 'EAST', 'EAST', 'EAST']
        self.assertEquals(expected, actions)
