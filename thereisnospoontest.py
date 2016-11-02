import unittest
import time
import sys
import thereisnospoon as tisn


class Test(unittest.TestCase):

    def test_detect_crossed_links(self):
        cell_matrix = ['..1..1',
                       '......',
                       '1...1.',
                       '......',
                       '..1..1']
        width = 6
        height = 5
        graph = tisn.Graph(cell_matrix, width, height)

        n1 = graph.get_point(2, 0)
        n2 = graph.get_point(2, 4)
        graph.add_link(n1, n2)
        n3 = graph.get_point(0, 2)
        n4 = graph.get_point(4, 2)
        graph.add_link(n3, n4)
        crosses = graph.is_link_crossing_other_links(n1, n2)
        self.assertTrue(crosses)
        same_cross = graph.is_link_crossing_other_links(n3, n4)
        self.assertTrue(same_cross)

    def test_no_cross(self):
        cell_matrix = ['..1..1',
                       '......',
                       '1...1.',
                       '......',
                       '..1..1']
        width = 6
        height = 5
        graph = tisn.Graph(cell_matrix, width, height)

        n1 = graph.get_point(0, 2)
        n2 = graph.get_point(4, 2)
        graph.add_link(n1, n2)
        n3 = graph.get_point(5, 0)
        n4 = graph.get_point(5, 4)
        graph.add_link(n3, n4)
        self.assertFalse(graph.is_link_crossing_other_links(n1, n2))

    def test_simple(self):
        cell_matrix = ['1.3',
                       '...',
                       '123']
        width = len(cell_matrix[0])
        height = len(cell_matrix)
        graph = tisn.Graph(cell_matrix, width, height)
        solutions = tisn.find_sol_main(graph)
        n1 = graph.get_point(0, 0)
        n2 = graph.get_point(2, 0)
        self.assertEquals(1, graph.nb_links(n1, n2), 'There should be only one link between ' + str(n1) + ' and ' + str(n2))
        self.assertEquals(5, len(solutions), 'There should be only 5 links to place, found ' + str(len(solutions)))

    def test_basic(self):
        cell_matrix = ['14.3',
                       '....',
                       '.4.4']
        width = 4
        height = 3
        graph = tisn.Graph(cell_matrix, width, height)
        solutions = tisn.find_sol_main(graph)
        n1 = graph.get_point(0, 3)
        n2 = graph.get_point(2, 3)
        self.assertEquals(8, len(solutions))

    def test_intermediate_three(self):
        print >> sys.stderr, 'Testing intermediate 3'
        cell_matrix = ['25.1',
                       '47.4',
                       '..1.',
                       '3344']
        width = 4
        height = 4
        graph = tisn.Graph(cell_matrix, width, height)
        solutions = tisn.find_sol_main(graph)
        self.assertTrue(solutions is not None)

    def test_island_creation(self):
      cell_matrix = ['21',
                     '21']
      width = len(cell_matrix[0])
      height = len(cell_matrix)
      graph = tisn.Graph(cell_matrix, width, height)
      node1 = graph.get_point(1, 0)
      node2 = graph.get_point(1, 1)
      will_create = graph.link_will_not_create_an_island(node1, node2)
      self.assertFalse(will_create, 'Link would create an island.')

      node3 = graph.get_point(0, 0)
      node4 = graph.get_point(0, 1)
      will_create = graph.link_will_not_create_an_island(node3, node4)
      self.assertTrue(will_create, 'Link would not create an island.')

    def test_obvious_links(self):
      """ This test should not need recursion. We check that
      it returns the appropriate number of links after the
      first optimization calls."""

      cell_matrix = ['22221',
                     '2....',
                     '22221']
      width = len(cell_matrix[0])
      height = len(cell_matrix)
      graph = tisn.Graph(cell_matrix, width, height)
      solutions = []
      tisn.remove_obvious_solutions(graph, solutions)
      print >> sys.stderr, 'Final graph: ' + str(graph)
      self.assertEquals(10, len(solutions))

    def test_cg(self):
        print >> sys.stderr, 'Testing CG...'
        cell_matrix = ['22221',
                       '2....',
                       '2....',
                       '2....',
                       '2....',
                       '22321',
                       '.....',
                       '.....',
                       '22321',
                       '2....',
                       '2....',
                       '2.131',
                       '2..2.',
                       '2222.']
        width = len(cell_matrix[0])
        height = len(cell_matrix)
        graph = tisn.Graph(cell_matrix, width, height)
        start = time.clock()
        solutions = tisn.find_sol_main(graph)
        time_sol = time.clock() - start
        self.assertTrue(time_sol < 1)

    def test_intermediate_three_other(self):
      cell_matrix = ['3..41',
                     '.22..',
                     '..1.1',
                     '.2.2.',
                     '3...3']
      width = len(cell_matrix[0])
      height = len(cell_matrix)
      graph = tisn.Graph(cell_matrix, width, height)
      solutions = tisn.find_sol_main(graph)
      self.assertEquals(12, len(solutions))


if __name__ == '__main__':
    unittest.main()
