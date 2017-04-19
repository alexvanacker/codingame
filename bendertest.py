import unittest
import time
import sys
import bender

class Test(unittest.TestCase):


    def testMapInit(self):
        map_array = ['#####',
                     '#@  #',
                     '#   #',
                     '#   #',
                     '#####']
        l = 5
        c = 5
        map = bender.Map(map_array,l,c)
        self.assertEquals('@', map.get(1,1))
        self.assertEquals((1,1), map.get_starting_point())
