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

    def testSimpleCorner(self):
        map_array = ['#####',
                     '#$  #',
                     '#   #',
                     '#@  #',
                     '#####']
        lines = 5
        columns = 5
        actions = bender.process(map_array, lines, columns)
        self.assertEquals(['EAST', 'EAST',
                           'NORTH', 'NORTH',
                           'WEST', 'WEST'], actions)

    def testInverter(self):
        map_array = ['#####',
                     '#$  #',
                     '#  @#',
                     '#  I#',
                     '#####']
        lines = 5
        columns = 5
        actions = bender.process(map_array, lines, columns)
        self.assertEquals(['SOUTH', 'WEST',
                           'WEST', 'NORTH',
                           'NORTH'], actions)

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
